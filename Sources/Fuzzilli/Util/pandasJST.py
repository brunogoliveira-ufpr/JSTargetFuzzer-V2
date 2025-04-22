import pandas as pd


# Define the path to the CSV file
file_path = '/home/kali/simple-seccov-log.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Conversão para datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Definição do índice
df.set_index('Timestamp', inplace=True)

# Resample para contagem de ocorrências a cada 10 minutos
resampled_df = df.resample('1T').size()

# Exibição do resultado
print(resampled_df)
