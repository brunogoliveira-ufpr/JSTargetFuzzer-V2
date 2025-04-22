import os
from datetime import datetime, timedelta

def get_files_by_weight_and_time(directory):
    """Função para retornar a contagem de arquivos com base no peso especificado (ou peso 1 por padrão) e agrupá-los por hora, independentemente do dia."""
    # Dicionário para armazenar a contagem por intervalo de tempo para cada peso
    time_groups_by_weight = {1: {}}

    files = os.listdir(directory)

    for file in files:
        file_path = os.path.join(directory, file)

        # Se o arquivo contém _weight_X, extrai o peso; caso contrário, considera peso 1
        if '_weight_' in file:
            try:
                weight_value = int(file.split('_weight_')[-1].replace('.txt', ''))
            except ValueError:
                weight_value = 1  # Caso o parsing falhe, considera peso 1
        else:
            weight_value = 1

        # Adiciona o dicionário para o peso se ele ainda não existir
        if weight_value not in time_groups_by_weight:
            time_groups_by_weight[weight_value] = {}

        # Obtém o timestamp de modificação do arquivo
        modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))

        # Ajusta o timestamp para apenas a hora do dia, ignorando a data
        rounded_hour = modification_time.hour - (modification_time.hour % 2)
        time_group = f'{rounded_hour:02}:00 - {rounded_hour + 2:02}:00'

        # Incrementa a contagem do grupo de tempo para o peso atual
        if time_group in time_groups_by_weight[weight_value]:
            time_groups_by_weight[weight_value][time_group] += 1
        else:
            time_groups_by_weight[weight_value][time_group] = 1

    return time_groups_by_weight

def format_output_by_interval(time_groups_by_weight):
    """Formata a saída para exibir os intervalos de tempo por hora, independentemente do dia."""
    for weight_value, files_by_time in time_groups_by_weight.items():
        sorted_times = sorted(files_by_time.keys())
        print(f"Arquivos com peso {weight_value} agrupados por intervalo de 2 horas (independente do dia):")
        for time_group in sorted_times:
            print(f"{time_group}: {files_by_time[time_group]} arquivos")
        print()  # Linha final em branco para separar grupos de diferentes pesos

# Diretório dos arquivos
directory ="/home/kali/JSTargetFuzzer-main/programs/files-fuzzilli/files"

# Contagem de arquivos agrupados por hora, independentemente da data
time_groups_by_weight = get_files_by_weight_and_time(directory)

# Formatar a saída
format_output_by_interval(time_groups_by_weight)
