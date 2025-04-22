import Foundation

public class MutationEngine: ComponentBase, FuzzEngine {
    private let numConsecutiveMutations: Int
    private var secCoverageHandler: SecCoverageHandler!
    private let statisticsService: StatisticsService

    public init(numConsecutiveMutations: Int) {
        self.numConsecutiveMutations = numConsecutiveMutations
        self.statisticsService = StatisticsService.getInstance(for: "MutationEngine")
        super.init(name: "MutationEngine")
    }

    override func initialize() {
        super.initialize()
        secCoverageHandler = SecCoverageHandler(fuzzer: fuzzer, logger: logger, engineName: "MutationEngine")
    }

    public func fuzzOne(_ group: DispatchGroup) {
        //statisticsService.log(LogMessages.mutationStart())

        var parent = fuzzer.corpus.randomElementForMutating()
        //statisticsService.log(LogMessages.selectedParentProgram())

        parent = prepareForMutating(parent)
        for i in 0..<numConsecutiveMutations {
            //statisticsService.log(LogMessages.mutationAttempt(attempt: i, maxAttempts: numConsecutiveMutations))

            var mutator = fuzzer.mutators.randomElement()
            let maxAttempts = 10
            var mutatedProgram: Program? = nil

            for attempt in 0..<maxAttempts {
                //statisticsService.log(LogMessages.mutationAttempt(attempt: attempt, maxAttempts: maxAttempts))

                if let result = mutator.mutate(parent, for: fuzzer) {
                    result.contributors.formUnion(parent.contributors)
                    mutator.addedInstructions(result.size - parent.size)
                    mutatedProgram = result
                    //statisticsService.log(LogMessages.mutationSuccessful())
                    break
                } else {
                    mutator.failedToGenerate()
                    mutator = fuzzer.mutators.randomElement()
                   // statisticsService.log(LogMessages.mutationFailed())
                }
            }

            guard let program = mutatedProgram else {
                //statisticsService.log(LogMessages.couldNotMutateSample(sample: FuzzILLifter().lift(parent)))
                continue
            }

            assert(program !== parent)
            let outcome = execute(program, secCoverageHandler: secCoverageHandler)
            //statisticsService.log(LogMessages.mutationOutcome(outcome: outcome))

            if .succeeded == outcome {
                //statisticsService.log(LogMessages.checkingCoverage())

                //secCoverageHandler.checkAndHandleCoverage(for: program, context: "MutationEngine - after execution")
                //statisticsService.log(LogMessages.coverageHandled())

                // Log raw data for each successful mutation
                //statisticsService.logRawData(program: program, fuzzer: fuzzer, engineName: "MutationEngine")

                parent = program
            }
        }
    }

    private func prepareForMutating(_ program: Program) -> Program {
        let b = fuzzer.makeBuilder()
        b.buildPrefix()

        //secCoverageHandler.checkAndHandleCoverage(for: program, context: "MutationEngine - during preparation")
        //statisticsService.log(LogMessages.coverageHandled())

        //program.numSeccov = fuzzer.evaluator.numSecPerEdge
        //program.numSeccov = fuzzer.evaluator.numSecPerEdge
        //program.numSeccov = fuzzer.evaluator.numSecPerEdge
        b.append(program)

        return b.finalize()
    }
}
