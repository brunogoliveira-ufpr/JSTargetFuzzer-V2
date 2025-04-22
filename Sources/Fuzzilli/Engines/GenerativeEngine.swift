import Foundation

public class GenerativeEngine: ComponentBase, FuzzEngine {
    private let numInstructionsToGenerate = 10
    private var secCoverageHandler: SecCoverageHandler!

    public init() {
        super.init(name: "GenerativeEngine")
    }

    override func initialize() {
        super.initialize()
        secCoverageHandler = SecCoverageHandler(fuzzer: fuzzer, logger: logger, engineName: "GenerativeEngine")
    }

    public func fuzzOne(_ group: DispatchGroup) {
        let b = fuzzer.makeBuilder()
        b.buildPrefix()
        b.build(n: numInstructionsToGenerate, by: .generating)

        let program = b.finalize()
        
        //secCoverageHandler.checkAndHandleCoverage(for: program, context: "GenerativeEngine - before execution")

        //let outcome = execute(program, secCoverageHandler: secCoverageHandler)

        let _ = execute(program, secCoverageHandler: secCoverageHandler)

        //secCoverageHandler.checkAndHandleCoverage(for: program, context: "GenerativeEngine - after execution")

        // Log raw data for the program
        //StatisticsService.getInstance(for: "GenerativeEngine").logRawData(program: program, fuzzer: fuzzer, engineName: "GenerativeEngine")
    }
}