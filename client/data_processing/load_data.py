import pandas as pd

def load_data(file_path):
    """Loads data from a CSV file and converts 'Timestamp' column to datetime if it exists."""
    df = pd.read_csv(file_path)
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df
