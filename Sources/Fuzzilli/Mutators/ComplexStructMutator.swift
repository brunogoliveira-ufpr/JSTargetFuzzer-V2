// A mutator that generates complex nested structures and combines multiple operations.
public class ComplexStructMutator: BaseInstructionMutator {
    private var deadCodeAnalyzer = DeadCodeAnalyzer()
    private var variableAnalyzer = VariableAnalyzer()
    private let minVisibleVariables = 3

    public init() {
        super.init(maxSimultaneousMutations: defaultMaxSimultaneousCodeGenerations)
        assert(defaultCodeGenerationAmount >= ProgramBuilder.minBudgetForRecursiveCodeGeneration)
    }

    public override func beginMutation(of program: Program) {
        deadCodeAnalyzer = DeadCodeAnalyzer()
        variableAnalyzer = VariableAnalyzer()
    }

    public override func canMutate(_ instr: Instruction) -> Bool {
        deadCodeAnalyzer.analyze(instr)
        variableAnalyzer.analyze(instr)
        // We can only generate code if there are some visible variables to use, and it only
        // makes sense to generate code if we're not currently in dead code.
        return variableAnalyzer.visibleVariables.count >= minVisibleVariables && !deadCodeAnalyzer.currentlyInDeadCode
    }

    public override func mutate(_ instr: Instruction, _ b: ProgramBuilder) {
        b.adopt(instr)
        assert(b.numberOfVisibleVariables >= minVisibleVariables)
        b.build(n: defaultCodeGenerationAmount, by: .generating)
    }
}
