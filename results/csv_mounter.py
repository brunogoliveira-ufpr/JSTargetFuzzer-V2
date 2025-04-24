import pandas as pd
import sys
from datetime import datetime, timedelta

def process_csvs(file_list, output_file):
    required_columns = ['NumSecCov', 'NumSecCovTotal']
    dfs = []

    for i, file in enumerate(file_list):
        df = pd.read_csv(file)

        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col} in file {file}")

        df = df[required_columns].copy()
        df = df.rename(columns={
            'NumSecCov': f'NumSecCov_{i+1}',
            'NumSecCovTotal': f'NumSecCovTotal_{i+1}'
        })
        dfs.append(df)

    # Align to shortest file length
    min_len = min(len(df) for df in dfs)
    dfs = [df.iloc[:min_len].reset_index(drop=True) for df in dfs]
    df_combined = pd.concat(dfs, axis=1)

    # Generate full timestamps from 2025-04-11 00:00:00 to 2025-04-11 23:59:59
    start_time = datetime.strptime("2025-04-11 00:00:00", "%Y-%m-%d %H:%M:%S")
    step = int((24 * 60 * 60) / min_len)  # seconds per step
    timestamps = [(start_time + timedelta(seconds=i * step)).strftime("%Y-%m-%d %H:%M:%S") for i in range(min_len)]
    df_combined.insert(0, 'Timestamp', timestamps)

    # Compute stats
    numseccov_cols = [f'NumSecCov_{i+1}' for i in range(5)]
    numseccovtotal_cols = [f'NumSecCovTotal_{i+1}' for i in range(5)]

    df_combined['Min_NumSecCov'] = df_combined[numseccov_cols].min(axis=1).cummax()
    df_combined['Mean_NumSecCov'] = df_combined[numseccov_cols].mean(axis=1).cummax()
    df_combined['Min_NumSecCovTotal'] = df_combined[numseccovtotal_cols].min(axis=1).cummax()
    df_combined['Mean_NumSecCovTotal'] = df_combined[numseccovtotal_cols].mean(axis=1).cummax()

    # Prepare output
    df_output = df_combined[['Timestamp',
                             'Min_NumSecCov',
                             'Min_NumSecCovTotal',
                             'Mean_NumSecCov',
                             'Mean_NumSecCovTotal']].copy()

    df_output.rename(columns={
        'Mean_NumSecCov': 'UniqueHitCount',
        'Mean_NumSecCovTotal': 'HitCount'
    }, inplace=True)

    df_output.to_csv(output_file, index=False)
    print(f"✅ Saved data with timestamp format '2025-04-11 HH:MM:SS' to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python3 csv_mounter.py file1.csv file2.csv file3.csv file4.csv file5.csv output.csv")
        sys.exit(1)

    file_list = sys.argv[1:6]
    output_file = sys.argv[6]
    process_csvs(file_list, output_file)
