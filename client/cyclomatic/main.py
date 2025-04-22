from concurrent.futures import ProcessPoolExecutor, as_completed
from config import MAX_WORKERS, CODE_FILES_DIRECTORY
from file_processing import get_files_in_batches, process_files_batch
from cyclomatic_analysis import save_general_analysis
from group_analysis import analyze_by_group_and_weight

def main():
    # Obter arquivos em lotes
    batches = get_files_in_batches()

    all_results = []
    file_weights = []  # Lista para armazenar os pesos de cada arquivo processado

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_files_batch, batch) for batch in batches]

        for future in as_completed(futures):
            try:
                result = future.result()
                all_results.extend(result)
                if result:
                    file_weights.extend([res['weight'] for res in result if 'weight' in res])  # Coletar os pesos dos arquivos processados
            except Exception as e:
                print(f"Erro durante o processamento de um lote: {e}")

    # Salvar análise geral
    save_general_analysis(all_results, file_weights)
    # print(all_results)
    # print(all_results)
    # Analisar por grupos e pesos, e gerar CSVs
    grouped_results = analyze_by_group_and_weight(all_results, file_weights, CODE_FILES_DIRECTORY)  # Passar file_weights também

    # Imprimir resumo geral das médias

    # print_general_summary(grouped_results)

if __name__ == "__main__":
    main()
