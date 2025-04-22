import os
import pandas as pd
from datetime import datetime, timedelta
from config import *

def get_file_count_by_weight(directory, weight_value):
    """Função para contar a quantidade de arquivos com base no peso especificado."""
    files = [f for f in os.listdir(directory) if f.endswith(f'_weight_{weight_value}.txt')]
    return len(files)

def assign_sequential_blocks(df):
    """
    Atribui blocos de 2 horas de forma sequencial, começando da modificação mais antiga.
    Cada bloco cobre 2 horas de arquivos ordenados pela data de modificação.
    """
    # Ordenar os arquivos pela data de modificação
    df = df.sort_values(by='modification_date')

    # Definir o primeiro bloco e o início do bloco
    block_number = 1
    current_block_start = df['modification_date'].iloc[0]  # Data de modificação mais antiga
    current_block_end = current_block_start + timedelta(hours=2)

    # Inicializar a lista para armazenar os números dos blocos
    block_numbers = []

    for mod_date in df['modification_date']:
        # Se a data de modificação estiver dentro do bloco atual, atribuir o bloco
        if mod_date <= current_block_end:
            block_numbers.append(block_number)
        else:
            # Se a data de modificação ultrapassar o bloco atual, iniciar um novo bloco
            block_number += 1
            current_block_start = current_block_end
            current_block_end = current_block_start + timedelta(hours=2)
            block_numbers.append(block_number)

    # Adicionar os números de blocos ao DataFrame
    df['2_hour_block'] = block_numbers
    return df

def analyze_by_group_and_weight(results, file_weights, directory):
    df = pd.DataFrame(results)

    # Verificar se as colunas esperadas estão presentes
    if 'qty' not in df.columns or 'cyclomatic_complexity' not in df.columns or 'modification_date' not in df.columns:
        print(f"Erro: Colunas 'qty', 'cyclomatic_complexity' ou 'modification_date' não estão presentes.")
        print(f"Colunas disponíveis: {df.columns.tolist()}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

    # Converter 'modification_date' para datetime
    df['modification_date'] = pd.to_datetime(df['modification_date'])

    # Atribuir cada modificação a um bloco de 2 horas sequencial, ignorando a data
    df = assign_sequential_blocks(df)

    # Obter a contagem total de arquivos para cada peso
    qty_files_weight_1 = get_file_count_by_weight(directory, 1)
    qty_files_weight_1000 = get_file_count_by_weight(directory, 1000)
    print(qty_files_weight_1, qty_files_weight_1000)
    # Agrupar por bloco de 2 horas, operação e peso, e contar o número de arquivos por peso
    grouped_analysis = df.groupby(['2_hour_block', 'operation', 'weight']).agg(
        sum_qty=('qty', 'sum'),
        total_complexity=('cyclomatic_complexity', 'sum'),
        file_count=('weight', 'size'),  # Contagem baseada nos pesos no DataFrame
        min_qty=('qty', 'min'),
        max_qty=('qty', 'max'),
        min_complexity=('cyclomatic_complexity', 'min'),
        max_complexity=('cyclomatic_complexity', 'max'),
        std_qty=('qty', lambda x: x.std(ddof=0)),  # Desvio padrão corrigido (ddof=0)
        std_complexity=('cyclomatic_complexity', lambda x: x.std(ddof=0))  # Desvio padrão corrigido (ddof=0)
    ).reset_index()

    # Verificar se a contagem de arquivos por peso é maior que zero antes de calcular as médias
    grouped_analysis['avg_qty_by_weight'] = grouped_analysis.apply(
        lambda row: row['sum_qty'] / qty_files_weight_1 if row['weight'] == 1 and qty_files_weight_1 > 0 else (
            row['sum_qty'] / qty_files_weight_1000 if row['weight'] == 1000 and qty_files_weight_1000 > 0 else 0), axis=1
    )
    grouped_analysis['avg_complexity_by_weight'] = grouped_analysis.apply(
        lambda row: row['total_complexity'] / qty_files_weight_1 if row['weight'] == 1 and qty_files_weight_1 > 0 else (
            row['total_complexity'] / qty_files_weight_1000 if row['weight'] == 1000 and qty_files_weight_1000 > 0 else 0), axis=1
    )

    # Separar os resultados por peso 1 e peso 1000 e salvar em arquivos CSV diferentes
    grouped_analysis_weight_1 = grouped_analysis[grouped_analysis['weight'] == 1]
    grouped_analysis_weight_1000 = grouped_analysis[grouped_analysis['weight'] == 1000]

    grouped_analysis_weight_1.to_csv('analysis_weight_1_by_2_hour_blocks.csv', index=False)
    grouped_analysis_weight_1000.to_csv('analysis_weight_1000_by_2_hour_blocks.csv', index=False)

    print("Análise por operação, peso, e blocos de 2 horas concluída e salva em arquivos separados.")

    return grouped_analysis

# Chamando a função para calcular e exibir os resultados
_1000 = get_file_count_by_weight('/home/kali/JSTargetFuzzer-main/programs/files/files', 1000)
_1 = get_file_count_by_weight('/home/kali/JSTargetFuzzer-main/programs/files/files', 1)

print(_1000)
print(_1)
