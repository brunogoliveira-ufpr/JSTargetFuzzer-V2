import pandas as pd

# Defina o caminho do arquivo TXT ou CSV
file_path = '/home/kali/JSTargetFuzzer-main/cli/I_Frota_por_UF_Municipio_Marca_e_Modelo_Ano_Novembro_2023.txt'

# Leia o arquivo CSV ou TXT delimitado por ';'
df = pd.read_csv(file_path, delimiter=';')

# Agrupe por "Município", "Marca Modelo" e "Ano Fabricação Veículo CRV", somando a "Qtd. Veículos"
grouped_data = df.groupby(["Município", "Marca Modelo", "Ano Fabricação Veículo CRV"])["Qtd. Veículos"].sum().reset_index()

# Filtre apenas o modelo que contém "Voyage Sport"
voyage_sport_data = grouped_data[grouped_data["Marca Modelo"].str.contains("Voyage Sport", case=False, na=False)]

# Exiba o resultado
print(voyage_sport_data)
