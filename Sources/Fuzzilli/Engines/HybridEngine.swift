import Foundation

public class HybridEngine: ComponentBase, FuzzEngine {
    private let numConsecutiveMutations: Int
    private let statisticsService: StatisticsService

    // Enum para diferentes resultados de geração de código
    private enum CodeGenerationOutcome: String, CaseIterable {
        case success = "Success"
        case generatedCodeFailed = "Generated code failed"
        case generatedCodeTimedOut = "Generated code timed out"
        case generatedCodeCrashed = "Generated code crashed"
    }

    // Contador para resultados de geração de código
    private var outcomeCounts = [CodeGenerationOutcome: Int]()
    
    // Estatísticas adicionais sobre os programas gerados
    private var totalInstructionsGenerated = 0
    private var programsGenerated = 0
    private var percentageOfGuardedOperationsAfterCodeGeneration = MovingAverage(n: 1000)
    private var percentageOfGuardedOperationsAfterCodeRefining = MovingAverage(n: 1000)

    // Mutador usado para "corrigir" os programas gerados com base nas informações de tempo de execução
    private var fixupMutator = FixupMutator(name: "HybridEngineFixupMutator")

    private var secCoverageHandler: SecCoverageHandler!

    public init(numConsecutiveMutations: Int) {
        self.numConsecutiveMutations = numConsecutiveMutations
        self.statisticsService = StatisticsService.getInstance(for: "HybridEngine")
        super.init(name: "HybridEngine")

        for outcome in CodeGenerationOutcome.allCases {
            outcomeCounts[outcome] = 0
        }
    }

    override func initialize() {
        super.initialize()
        secCoverageHandler = SecCoverageHandler(fuzzer: fuzzer, logger: logger, engineName: "HybridEngine")

        if fuzzer.config.logLevel.isAtLeast(.verbose) {
            fuzzer.timers.scheduleTask(every: 30 * Minutes) {
                guard self.programsGenerated > 0 else { return }

                self.logger.verbose("Program Template Statistics:")
                let nameMaxLength = self.fuzzer.programTemplates.map({ $0.name.count }).max()!
                for template in self.fuzzer.programTemplates {
                    let name = template.name.rightPadded(toLength: nameMaxLength)
                    let correctnessRate = String(format: "%.2f%%", template.correctnessRate * 100).leftPadded(toLength: 7)
                    let interestingSamplesRate = String(format: "%.2f%%", template.interestingSamplesRate * 100).leftPadded(toLength: 7)
                    let timeoutRate = String(format: "%.2f%%", template.timeoutRate * 100).leftPadded(toLength: 6)
                    let avgInstructionsAdded = String(format: "%.2f", template.avgNumberOfInstructionsGenerated).leftPadded(toLength: 5)
                    let samplesGenerated = template.totalSamples
                    self.logger.verbose("    \(name) : Correctness rate: \(correctnessRate), Interesting sample rate: \(interestingSamplesRate), Timeout rate: \(timeoutRate), Avg. # of instructions generated: \(avgInstructionsAdded), Total # of generated samples: \(samplesGenerated)")
                }

                let totalOutcomes = self.outcomeCounts.values.reduce(0, +)
                self.logger.verbose("Frequencies of code generation outcomes:")
                for outcome in CodeGenerationOutcome.allCases {
                    let count = self.outcomeCounts[outcome]!
                    let frequency = (Double(count) / Double(totalOutcomes)) * 100.0
                    self.logger.verbose("    \(outcome.rawValue.rightPadded(toLength: 25)): \(String(format: "%.2f%%", frequency))")
                }

                self.logger.verbose("Number of generated programs: \(self.programsGenerated)")
                self.logger.verbose("Average programs size: \(self.totalInstructionsGenerated / self.programsGenerated)")
                self.logger.verbose("Average percentage of guarded operations after code generation: \(String(format: "%.2f%", self.percentageOfGuardedOperationsAfterCodeGeneration.currentValue))%")
                self.logger.verbose("Average percentage of guarded operations after code refining: \(String(format: "%.2f%", self.percentageOfGuardedOperationsAfterCodeRefining.currentValue))%")
            }
        }
    }

    private func generateTemplateProgram(template: ProgramTemplate) -> Program {
        let b = fuzzer.makeBuilder(mode: .conservative)
        b.traceHeader("Generating program based on \(template.name) template")
        template.generate(in: b)
        let program = b.finalize()

        program.contributors.insert(template)
        template.addedInstructions(program.size)
        return program
    }

    public func fuzzOne(_ group: DispatchGroup) {
        let template = fuzzer.programTemplates.randomElement()
        let generatedProgram = generateTemplateProgram(template: template)

        // Atualiza as estatísticas básicas de geração de código
        totalInstructionsGenerated += generatedProgram.size
        programsGenerated += 1
        percentageOfGuardedOperationsAfterCodeGeneration.add(computePercentageOfGuardedOperations(in: generatedProgram))

        let outcome = execute(generatedProgram, withTimeout: fuzzer.config.timeout * 2, secCoverageHandler: secCoverageHandler)
        switch outcome {
        case .succeeded:
            recordOutcome(.success)
        case .failed:
            return recordOutcome(.generatedCodeFailed)
        case .timedOut:
            return recordOutcome(.generatedCodeTimedOut)
        case .crashed:
            return recordOutcome(.generatedCodeCrashed)
        }

        let refinedProgram: Program
        if let result = fixupMutator.mutate(generatedProgram, for: fuzzer) {
            refinedProgram = result
            percentageOfGuardedOperationsAfterCodeRefining.add(computePercentageOfGuardedOperations(in: refinedProgram))
        } else {
            refinedProgram = generatedProgram
        }

        var parent = refinedProgram
        for _ in 0..<numConsecutiveMutations {
            var mutator = fuzzer.mutators.randomElement()
            let maxAttempts = 10
            var mutatedProgram: Program? = nil
            for _ in 0..<maxAttempts {
                if let result = mutator.mutate(parent, for: fuzzer) {
                    result.contributors.formUnion(parent.contributors)
                    mutator.addedInstructions(result.size - parent.size)
                    mutatedProgram = result
                    break
                } else {
                    mutator.failedToGenerate()
                    mutator = fuzzer.mutators.randomElement()
                }
            }

            guard let program = mutatedProgram else {
                logger.warning("Could not mutate sample, giving up. Sample:\n\(FuzzILLifter().lift(parent))")
                continue
            }

            assert(program !== parent)
            let outcome = execute(program, secCoverageHandler: secCoverageHandler)

            if .succeeded == outcome {
                parent = program
            }
        }

        // Log raw data for each program
        statisticsService.logRawData(program: parent, fuzzer: fuzzer, engineName: "HybridEngine")
    }

    private func recordOutcome(_ outcome: CodeGenerationOutcome) {
        outcomeCounts[outcome]! += 1
    }

    private func computePercentageOfGuardedOperations(in program: Program) -> Double {
        let numGuardedOperations = Double(program.code.filter({ $0.isGuarded }).count)
        // Também contamos blocos try-catch como guardas para fins dessas estatísticas, e os contamos como 3 instruções
        // pois eles precisam pelo menos do BeginTry e EndTryCatchFinally, além de um BeginCatch ou BeginFinally.
        let numTryCatchBlocks = Double(program.code.filter({ $0.op is BeginTry }).count)
        return ((numGuardedOperations + numTryCatchBlocks * 3) / Double(program.size)) * 100.0
    }
}
