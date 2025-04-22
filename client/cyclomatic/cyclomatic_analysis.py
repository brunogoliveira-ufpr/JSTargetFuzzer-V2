import pandas as pd

def save_general_analysis(results, file_weights):
    # Converter os resultados para um DataFrame
    df = pd.DataFrame(results)

    # Salvar o DataFrame inicial
    df.to_csv('results.csv', index=False, columns=['operation', 'qty', 'weight', 'cyclomatic_complexity'])

    # Cálculo da quantidade total e média de quantidade por operação e por peso
    grouped = df.groupby(['operation', 'weight']).agg(
        sum_qty=('qty', 'sum'), 
        avg_qty=('qty', 'mean'),
        total_complexity=('cyclomatic_complexity', 'sum')
    ).reset_index()

    # Salvar o DataFrame com as quantidades totais e médias e complexidade ciclomática
    grouped.to_csv('sum_avg_complexity_by_op_and_weight.csv', index=False)

    # Cálculo de quantidade total de arquivos e quantidade por peso
    total_files = len(set(file_weights))
    files_by_weight = pd.Series(file_weights).value_counts().to_dict()

    # Exibir os resultados
    print(f"\nQuantidade total de arquivos processados: {total_files}")
    print("Quantidade de arquivos por peso:")
    for weight, count in files_by_weight.items():
        print(f"Peso {weight}: {count} arquivo(s)")

    print(f"\nProcessamento concluído. {len(results)} registros salvos em 'results.csv'.")
    print(f"Quantidade total, médias e complexidade ciclomática salvas em 'sum_avg_complexity_by_op_and_weight.csv'.")
