public class LogMessages {
    public static func mutationStart() -> String {
        return "[MutationEngine] Starting fuzzOne"
    }

    public static func selectedParentProgram() -> String {
        return "[MutationEngine] Selected parent program for mutation"
    }

    public static func mutationAttempt(attempt: Int, maxAttempts: Int) -> String {
        return "[MutationEngine] Attempt \(attempt + 1) of \(maxAttempts) to mutate program"
    }

    public static func mutationSuccessful() -> String {
        return "[MutationEngine] Mutation successful"
    }

    public static func mutationFailed() -> String {
        return "[MutationEngine] Mutation failed, trying another mutator"
    }

    public static func mutationOutcome(outcome: ExecutionOutcome) -> String {
        return "[MutationEngine] Execution outcome: \(outcome)"
    }

    public static func checkingCoverage() -> String {
        return "[MutationEngine] Checking coverage after successful mutation"
    }

    public static func coverageHandled() -> String {
        return "[MutationEngine] Coverage handled for program"
    }

    public static func couldNotMutateSample(sample: String) -> String {
        return "[MutationEngine] Could not mutate sample, giving up. Sample:\n\(sample)"
    }
}
