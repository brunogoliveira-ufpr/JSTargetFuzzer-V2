# config.py

# Caminho do diretório de arquivos
# CODE_FILES_DIRECTORY = "/home/kali/JSTargetFuzzer-main/programs/files/files"
# CODE_FILES_DIRECTORY = "/home/kali/JSTargetFuzzer-main/programs/files-fuzzilli/files"
CODE_FILES_DIRECTORY = "/home/kali/JSTargetFuzzer-main/programs/fuzzilli-duktape-files/files"
# CODE_FILES_DIRECTORY = "/home/kali/JSTargetFuzzer-main/programs/fuzzilli-duktape-files/files"
# CODE_FILES_DIRECTORY = "/home/kali/JSTargetFuzzer-main/programs/test/"
CSV_DIR = "/home/kali/JSTargetFuzzer-main/cli/cyclomatic/"


# Configurações gerais
BATCH_SIZE = 50000  # Tamanho dos lotes
MAX_WORKERS = 32  # Número de workers paralelos
                  
# Mapeamento de geradores para grupos
custom_op_group = {
    # Loops
    "ForInLoopGenerator": "Loops",
    "ForOfLoopGenerator": "Loops",
    "WhileLoopGenerator": "Loops",
    "DoWhileLoopGenerator": "Loops",
    "SimpleForLoopGenerator": "Loops",
    "ComplexForLoopGenerator": "Loops",
    "RepeatLoopGenerator": "Loops",
    "LoopBreakGenerator": "Loops",
    "ContinueGenerator": "Loops",
    "LoopContinueGenerator": "Loops",
    "LoopBeginGenerator": "Loops",
    "LoopEndGenerator": "Loops",

    # Numeric Operations
    "BinaryOperationGenerator": "Numeric Operations",
    "UnaryOperationGenerator": "Numeric Operations",
    "NumberComputationGenerator": "Numeric Operations",
    "ArithmeticOperationGenerator": "Numeric Operations",
    "ComparisonGenerator": "Numeric Operations",
    "TernaryOperationGenerator": "Numeric Operations",
    "UpdateExpressionGenerator": "Numeric Operations",
    "TypeofGenerator": "Numeric Operations",
    "InstanceofGenerator": "Numeric Operations",
    "BitwiseOperationGenerator": "Numeric Operations",
    "MathOperationGenerator": "Numeric Operations",

    # Variables
    "VariableDeclarationGenerator": "Variables",
    "VariableAssignmentGenerator": "Variables",
    "VariableReassignmentGenerator": "Variables",
    "DupGenerator": "Variables",
    "NamedVariableLoadGenerator": "Variables",
    "NamedVariableStoreGenerator": "Variables",
    "ReassignmentGenerator": "Variables",
    "StoreNamedVariableGenerator": "Variables",
    "LoadNamedVariableGenerator": "Variables",
    "DestructObjectGenerator": "Variables",
    "ObjectDestructuringGenerator": "Variables",
    "LoadIntegerGenerator": "Variables",
    "LoadFloatGenerator": "Variables",
    "LoadStringGenerator": "Variables",
    "LoadBooleanGenerator": "Variables",
    "LoadUndefinedGenerator": "Variables",
    "LoadNullGenerator": "Variables",
}