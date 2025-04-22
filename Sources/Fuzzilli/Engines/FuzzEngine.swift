import Foundation

public protocol FuzzEngine: ComponentBase {
    func fuzzOne(_ group: DispatchGroup)
}

extension FuzzEngine {
    public func execute(_ program: Program, withTimeout timeout: UInt32? = nil, secCoverageHandler: SecCoverageHandler) -> ExecutionOutcome {
        fuzzer.dispatchEvent(fuzzer.events.ProgramGenerated, data: program)

        let execution = fuzzer.execute(program, withTimeout: timeout, purpose: .fuzzing)

        switch execution.outcome {
            case .crashed(let termsig):
                fuzzer.processCrash(program, withSignal: termsig, withStderr: execution.stderr, withStdout: execution.stdout, origin: .local, withExectime: execution.execTime)
                program.contributors.generatedCrashingSample()

            case .succeeded:
                fuzzer.dispatchEvent(fuzzer.events.ValidProgramFound, data: program)
                var isInteresting = false

                if let aspects = fuzzer.evaluator.evaluate(execution) {
                    secCoverageHandler.checkAndHandleCoverage(for: program, context: "FuzzEngine - during evaluation")
                    if fuzzer.config.enableInspection {
                        program.comments.add("Program may be interesting due to \(aspects)", at: .footer)
                        program.comments.add("RUNNER ARGS: \(fuzzer.runner.processArguments.joined(separator: " "))", at: .header)
                    }
                    isInteresting = fuzzer.processMaybeInteresting(program, havingAspects: aspects, origin: .local)
                }
                StatisticsService.getInstance(for: "FuzzEngine").logRawData(program: program, fuzzer: fuzzer, engineName: "FuzzEngine")
                if isInteresting {
                    program.contributors.generatedInterestingSample()
                   //secCoverageHandler.checkChildWeight(for: program, context: "FuzzEngine - during evaluation")
                } else {
                    program.contributors.generatedValidSample()
                }

            case .failed(_):
                if fuzzer.config.enableDiagnostics {
                    program.comments.add("Stdout:\n" + execution.stdout, at: .footer)
                }
                fuzzer.dispatchEvent(fuzzer.events.InvalidProgramFound, data: program)
                program.contributors.generatedInvalidSample()

            case .timedOut:
                fuzzer.dispatchEvent(fuzzer.events.TimeOutFound, data: program)
                program.contributors.generatedTimeOutSample()
        }

        if fuzzer.config.enableDiagnostics {
            ensureDeterministicExecutionOutcomeForDiagnostic(of: program)
        }

        return execution.outcome
    }

    private func ensureDeterministicExecutionOutcomeForDiagnostic(of program: Program) {
        let execution1 = fuzzer.execute(program, purpose: .other)
        let stdout1 = execution1.stdout
        let execution2 = fuzzer.execute(program, purpose: .other)
        let stdout2 = execution2.stdout
        switch (execution1.outcome, execution2.outcome) {
        case (.succeeded, .failed(_)),
             (.failed(_), .succeeded):
            let stderr2 = execution2.stderr
            logger.warning("""
                [FuzzEngine] Non-deterministic execution detected for program
                \(fuzzer.lifter.lift(program))
                // Stdout of first execution
                \(stdout1)
                // Stderr of first execution
                \(execution1.stderr)
                // Stdout of second execution
                \(stdout2)
                // Stderr of second execution
                \(stderr2)
                """)
        default:
            break
        }
    }
}
