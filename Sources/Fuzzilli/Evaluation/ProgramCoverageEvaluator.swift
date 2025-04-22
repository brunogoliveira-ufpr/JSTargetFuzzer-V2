// Copyright 2019 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import Foundation
import libcoverage

/// Represents a set of newly discovered CFG edges in the target program.
public class CovEdgeSet: ProgramAspects {
    private var numEdges: UInt32
    fileprivate var edges: UnsafeMutablePointer<UInt32>?

    init(edges: UnsafeMutablePointer<UInt32>?, numEdges: UInt32) {
        self.numEdges = numEdges
        self.edges = edges
        super.init(outcome: .succeeded)   
    }
    deinit {
        free(edges)
    }

    /// The number of aspects is simply the number of newly discovered coverage edges.
    public override var count: UInt32 {
        return numEdges
    }

    public override var description: String {
        return "new coverage: \(count) newly discovered edge\(count > 1 ? "s" : "") in the CFG of the target"
    }

    /// Returns an array of all the newly discovered edges of this CovEdgeSet.
    ///
    /// This adds additional copies, but is only hit when new programs are added to the corpus
    /// It is used by corpus schedulers such as MarkovCorpus that require knowledge of which samples trigger which edges
    public func getEdges() -> [UInt32] {
        return Array(UnsafeBufferPointer(start: edges, count: Int(count)))
    }

    public static func == (lhsEdges: CovEdgeSet, rhsEdges: CovEdgeSet) -> Bool {
        if lhsEdges.outcome != rhsEdges.outcome { return false }
        if lhsEdges.count != rhsEdges.count { return false }
        for i in 0..<Int(lhsEdges.count) {
            if lhsEdges.edges![i] != rhsEdges.edges![i] {
                return false
            }
        }
        return true
    }

    // Updates the internal state to match the provided collection
    fileprivate func setEdges<T: Collection>(_ collection: T) where T.Element == UInt32 {
        precondition(collection.count <= self.count)
        self.numEdges = UInt32(collection.count)
        for (i, edge) in collection.enumerated() {
            self.edges![i] = edge
        }
    } 

}

public class ProgramCoverageEvaluator: ComponentBase, ProgramEvaluator {
    private static var instances = 0
    private var shouldTrackEdgeCounts: Bool
    private var resetCounts: [UInt32:UInt64] = [:]
    private let maxResetCount: UInt64 = 1000

    public var currentScore: Double {
        return Double(context.found_edges) / Double(context.num_edges)
    }

    public var isCovered: Bool {
        return context.found_sec_cov
    }
    
    public var numEdges: Double {
        return Double(context.num_edges)
    }

    public var numSecCov: Double {
        return Double(context.ctx_num_sec_cov)
    }

    public var numSecCovTotal: Double {
        return Double(context.ctx_num_sec_cov_total)
    }

    //public var numSecPerEdge: Double {
    //    return Double(context.ctx_num_sec_per_edge)
    //}

    //public var numSecPerEdgeTotal: Double {
    //    return Double(context.ctx_num_sec_per_edge_total_double)
    //}

    private var context = libcoverage.cov_context()

    public init(runner: ScriptRunner) {
        self.shouldTrackEdgeCounts = false
        super.init(name: "Coverage")

        let id = ProgramCoverageEvaluator.instances
        ProgramCoverageEvaluator.instances += 1

        context.id = Int32(id)
        guard libcoverage.cov_initialize(&context) == 0 else {
            fatalError("Could not initialize libcoverage")
        }
#if os(Windows)
        runner.setEnvironmentVariable("SHM_ID", to: "shm_id_\(GetCurrentProcessId())_\(id)")
#else
        runner.setEnvironmentVariable("SHM_ID", to: "shm_id_\(getpid())_\(id)")
#endif

    }

    public func enableEdgeTracking() {
        assert(!isInitialized)
        shouldTrackEdgeCounts = true
    }

    public func getEdgeHitCounts() -> [UInt32] {
        var edgeCounts = libcoverage.edge_counts()
        let result = libcoverage.cov_get_edge_counts(&context, &edgeCounts)
        if result == -1 {
            logger.error("Error retrieving smallest hit count edges")
            return []
        }
        var edgeArray = Array(UnsafeBufferPointer(start: edgeCounts.edge_hit_count, count: Int(edgeCounts.count)))

        for (edge, count) in resetCounts {
            if count >= maxResetCount {
                edgeArray[Int(edge)] = 0
            }
        }

        return edgeArray
    }

    override func initialize() {
        fuzzer.registerEventListener(for: fuzzer.events.PreExecute) { execution in
            libcoverage.cov_clear_bitmap(&self.context)
        }

        fuzzer.registerEventListener(for: fuzzer.events.Shutdown) { _ in
            libcoverage.cov_shutdown(&self.context)
        }

        let _ = fuzzer.execute(Program(), purpose: .startup)
        libcoverage.cov_finish_initialization(&context, shouldTrackEdgeCounts ? 1 : 0)
        logger.info("Initialized, \(context.num_edges) edges")
    }

    public func evaluate(_ execution: Execution) -> ProgramAspects? {
        assert(execution.outcome == .succeeded)
        var newEdgeSet = libcoverage.edge_set()
        let result = libcoverage.cov_evaluate(&context, &newEdgeSet)

        guard result != -1 else {
            logger.error("Could not evaluate sample")
            return nil
        }

        if result == 1 {
            return CovEdgeSet(edges: newEdgeSet.edge_indices, numEdges: newEdgeSet.count)
        } else {
            assert(newEdgeSet.edge_indices == nil && newEdgeSet.count == 0)
            return nil
        }
    }

    public func evaluateCrash(_ execution: Execution) -> ProgramAspects? {
        assert(execution.outcome.isCrash())
        let result = libcoverage.cov_evaluate_crash(&context)
        guard result != -1 else {
            logger.error("Could not evaluate crash")
            return nil
        }

        if result == 1 {
            return ProgramAspects(outcome: execution.outcome)
        } else {
            return nil
        }
    }

    public func hasAspects(_ execution: Execution, _ aspects: ProgramAspects) -> Bool {
        guard execution.outcome == aspects.outcome else {
            return false
        }

        if execution.outcome.isCrash() {
            return true
        }

        guard let edgeSet = aspects as? CovEdgeSet else {
            fatalError("Invalid aspects passed to hasAspects")
        }

        let result = libcoverage.cov_compare_equal(&context, edgeSet.edges, edgeSet.count)
        if result == -1 {
            logger.error("Could not compare program executions")
        }
        return result == 1
    }

    public func computeAspectIntersection(of program: Program, with aspects: ProgramAspects) -> ProgramAspects? {
        guard let firstCovEdgeSet = aspects as? CovEdgeSet else {
            logger.fatal("Coverage Evaluator received non coverage aspects")
        }

        resetAspects(firstCovEdgeSet)

        let execution = fuzzer.execute(program, purpose: .checkForDeterministicBehavior)
        guard execution.outcome == .succeeded else { return nil }
        guard let secondCovEdgeSet = evaluate(execution) as? CovEdgeSet else { return nil }

        let firstEdgeSet = Set(UnsafeBufferPointer(start: firstCovEdgeSet.edges, count: Int(firstCovEdgeSet.count)))
        let secondEdgeSet = Set(UnsafeBufferPointer(start: secondCovEdgeSet.edges, count: Int(secondCovEdgeSet.count)))

        for edge in secondEdgeSet.subtracting(firstEdgeSet) {
            resetEdge(edge)
        }

        let intersectedEdgeSet = secondEdgeSet.intersection(firstEdgeSet)
        guard intersectedEdgeSet.count != 0 else { return nil }

        let intersectedCovEdgeSet = secondCovEdgeSet
        intersectedCovEdgeSet.setEdges(intersectedEdgeSet)

        return intersectedCovEdgeSet
    }

    public func exportState() -> Data {
        var state = Data()
        state.append(Data(bytes: &context.num_edges, count: 4))
        state.append(Data(bytes: &context.bitmap_size, count: 4))
        state.append(Data(bytes: &context.found_edges, count: 4))
        state.append(context.virgin_bits, count: Int(context.bitmap_size))
        state.append(context.crash_bits, count: Int(context.bitmap_size))

        return state
    }

    public func importState(_ state: Data) throws {
        assert(isInitialized)
        let headerSize = 12

        guard state.count == headerSize + Int(context.bitmap_size) * 2 else {
            throw FuzzilliError.evaluatorStateImportError("Cannot import coverage state as it has an unexpected size. Ensure all instances use the same build of the target")
        }

        let numEdges = state.withUnsafeBytes { $0.load(fromByteOffset: 0, as: UInt32.self) }
        let bitmapSize = state.withUnsafeBytes { $0.load(fromByteOffset: 4, as: UInt32.self) }
        let foundEdges = state.withUnsafeBytes { $0.load(fromByteOffset: 8, as: UInt32.self) }

        guard bitmapSize == context.bitmap_size && numEdges == context.num_edges else {
            throw FuzzilliError.evaluatorStateImportError("Cannot import coverage state due to different bitmap sizes. Ensure all instances use the same build of the target")
        }

        context.found_edges = foundEdges

        var start = state.startIndex + headerSize
        state.copyBytes(to: context.virgin_bits, from: start..<start + Int(bitmapSize))
        start += Int(bitmapSize)
        state.copyBytes(to: context.crash_bits, from: start..<start + Int(bitmapSize))

        logger.info("Imported existing coverage state with \(foundEdges) edges already discovered")
    }

    public func resetState() {
        resetCounts = [:]
        libcoverage.cov_reset_state(&context)
    }

    private func resetEdge(_ edge: UInt32) {
        resetCounts[edge] = (resetCounts[edge] ?? 0) + 1
        if resetCounts[edge]! <= maxResetCount {
            libcoverage.cov_clear_edge_data(&context, edge)
        }
    }

    private func resetAspects(_ aspects: CovEdgeSet) {
        for i in 0..<Int(aspects.count) {
            resetEdge(aspects.edges![i])
        }
    }
}
