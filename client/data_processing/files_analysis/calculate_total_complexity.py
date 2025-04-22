import os
import re
import json
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial

# Caminhos para os arquivos JSON
complexity_json_path = os.path.join(os.path.dirname(__file__), 'cyclomatic_complexity.json')
mapping_json_path = os.path.join(os.path.dirname(__file__), 'operation_to_generator.json')
manual_mapping_json_path = os.path.join(os.path.dirname(__file__), 'manual_operation_mapping.json')

# Carregar os arquivos JSON
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

complexity_data = load_json(complexity_json_path)
operation_to_generator = load_json(mapping_json_path)
manual_operation_to_generator = load_json(manual_mapping_json_path)

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

# Regex para extrair operações
instruction_regex = re.compile(r'Fuzzilli\.Instruction\(op: Fuzzilli\.([A-Za-z]+),')

# Função para processar um único arquivo
def process_file(file_path, operation_to_generator, manual_operation_to_generator, generator_to_group, complexity_data, instruction_regex):
    results = []
    try:
        # Extrair o peso do nome do arquivo
        weight_match = re.search(r'_weight_(\d+)\.txt', file_path)
        weight = int(weight_match.group(1)) if weight_match else None

        # Ler o conteúdo do arquivo
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Extrair todas as operações
        operations = instruction_regex.findall(content)

        # Mapear as operações para os geradores e grupos, e calcular a complexidade
        for operation in operations:
            generator = operation_to_generator.get(operation, manual_operation_to_generator.get(operation, "Unknown"))
            group = generator_to_group.get(generator, "Unknown")
            complexity = complexity_data.get(generator, {}).get('cyclomatic_complexity', 0)

            results.append({
                'operation': operation,
                'generator': generator,
                'group': group,
                'weight': weight,
                'cyclomatic_complexity': complexity
            })
    except Exception as e:
        print(f"Erro ao processar o arquivo {file_path}: {e}")
    return results

# Função para processar arquivos em lotes
def process_files_batch(file_paths, operation_to_generator, manual_operation_to_generator, generator_to_group, complexity_data, instruction_regex):
    batch_results = []
    for file_path in file_paths:
        batch_results.extend(process_file(file_path, operation_to_generator, manual_operation_to_generator, generator_to_group, complexity_data, instruction_regex))
    return batch_results

# Função principal que organiza o processamento
def main():
    # Diretório contendo os arquivos
    code_files_directory = "/home/kali/JSTargetFuzzer-main/programs/"

    # Obter todos os arquivos no diretório
    all_files = [os.path.join(code_files_directory, f) for f in os.listdir(code_files_directory) if f.endswith('.txt')]

    # Definir o tamanho do lote para processamento em paralelo
    batch_size = 500  # Ajuste conforme necessário
    batches = [all_files[i:i + batch_size] for i in range(0, len(all_files), batch_size)]

    # Função parcial para facilitar a passagem de múltiplos argumentos
    func = partial(
        process_files_batch,
        operation_to_generator=operation_to_generator,
        manual_operation_to_generator=manual_operation_to_generator,
        generator_to_group=generator_to_group,
        complexity_data=complexity_data,
        instruction_regex=instruction_regex
    )

    all_results = []
    with ProcessPoolExecutor(max_workers=16) as executor:  # Ajuste max_workers conforme o número de CPUs disponíveis
        # Enviar lotes para processamento
        futures = [executor.submit(func, batch) for batch in batches]

        for future in as_completed(futures):
            try:
                result = future.result()
                all_results.extend(result)
            except Exception as e:
                print(f"Erro durante o processamento de um lote: {e}")

    # Converter os resultados para um DataFrame e salvar
    df = pd.DataFrame(all_results)
    df.to_csv('results.csv', index=False)
    print(f"Processamento concluído. {len(all_results)} registros salvos em 'results.csv'.")

if __name__ == "__main__":
    main()