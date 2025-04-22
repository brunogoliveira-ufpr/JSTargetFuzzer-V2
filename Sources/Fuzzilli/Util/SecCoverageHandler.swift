import Foundation

public var programWeight1: Double = 1000.0  // Pai 
public var programWeight2: Double = 250.0  // Filho
public var programWeight3: Double = 1.0  // Program default JST

public class SecCoverageHandler {
    private let fuzzer: Fuzzer
    private let logger: Logger
    private let statisticsService: StatisticsService
    private let engineName: String
    //private let duplicateHandler: DuplicateProgramHandler

    public init(fuzzer: Fuzzer, logger: Logger, engineName: String) {
        self.fuzzer = fuzzer
        self.logger = logger
        self.statisticsService = StatisticsService.getInstance(for: engineName)
        self.engineName = engineName
        //self.duplicateHandler = DuplicateProgramHandler()
    }

    /// Handles coverage updates for the program
    public func checkAndHandleCoverage(for program: Program, context: String) {
        if fuzzer.evaluator.isCovered {
            program.weight = programWeight1  
            //program.comments.add("[\(context)] Interesting", at: .footer)

            //if context.contains("after execution") || context.contains("during evaluation") {
            fuzzer.corpus.add(program, ProgramAspects(outcome: .succeeded))
            //}
        }
    }

    /// Handles child program weight verification
    public func checkChildWeight(for program: Program, context: String) {
        if program.weight == programWeight2 {
            logger.info("[JST] childProgram SecCovFound")
            fuzzer.corpus.add(program, ProgramAspects(outcome: .succeeded))
        }
    }
}
