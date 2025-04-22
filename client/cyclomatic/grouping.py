# grouping.py
import pandas as pd
import math

def group_by_weight_and_subgroups(df, weight_column='weight', max_group_size=2):
    """
    Agrupa os dados pelo peso e os divide em subgrupos de tamanho limitado.
    
    Parâmetros:
    df: DataFrame - os dados de entrada contendo os registros.
    weight_column: str - o nome da coluna que contém os valores de peso.
    max_group_size: int - o tamanho máximo de registros por subgrupo.
    
    Retorna:
    Uma lista de dicionários contendo os grupos separados por peso e seus subgrupos.
    """
    # Agrupar os dados pelo peso
    grouped_by_weight = df.groupby(weight_column)

    all_groups = []

    for weight, group in grouped_by_weight:
        # Ordenar o grupo por timestamp (opcional, caso faça sentido na sua lógica)
        group = group.sort_values(by='timestamp')

        # Determinar o número de subgrupos necessários com base no tamanho máximo de cada grupo
        num_records = len(group)
        num_subgroups = math.ceil(num_records / max_group_size)

        subgroups = []
        start_idx = 0
        for i in range(num_subgroups):
            end_idx = start_idx + max_group_size
            subgroup = group.iloc[start_idx:end_idx]
            subgroups.append(subgroup)
            start_idx = end_idx

        # Adicionar os subgrupos desse peso à lista final de todos os grupos
        all_groups.append({
            'weight': weight,
            'subgroups': subgroups
        })

    return all_groups
