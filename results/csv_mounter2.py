import pandas as pd
import sys
from datetime import datetime, timedelta

def even_sample_to_1440(df: pd.DataFrame) -> pd.DataFrame:
    df = df[['NumSecCov', 'NumSecCovTotal']].dropna()
    df = df.interpolate(method='linear', limit_direction='both')

    # Sample 1440 evenly spaced rows
    total_rows = len(df)
    if total_rows < 1440:
        # Pad with last row if too short
        pad = df.iloc[[-1]].copy()
        while len(df) < 1440:
            df = pd.concat([df, pad], ignore_index=True)
    else:
        step = total_rows / 1440
        indices = [int(i * step) for i in range(1440)]
        df = df.iloc[indices].reset_index(drop=True)

    return df

def process_csvs(file_list, output_file):
    dfs = []
    for i, file in enumerate(file_list):
        df = pd.read_csv(file)

        if 'NumSecCov' not in df.columns or 'NumSecCovTotal' not in df.columns:
            raise ValueError(f"Missing required columns in file: {file}")

        df_clean = even_sample_to_1440(df)
        df_clean = df_clean.rename(columns={
            'NumSecCov': f'NumSecCov_{i+1}',
            'NumSecCovTotal': f'NumSecCovTotal_{i+1}'
        })
        dfs.append(df_clean)

    # Merge all 5 datasets
    df_combined = pd.concat(dfs, axis=1)

    # Generate correct timestamp column
    start_time = datetime.strptime("2025-04-11 00:00:00", "%Y-%m-%d %H:%M:%S")
    timestamps = [(start_time + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(1440)]
    df_combined.insert(0, 'Timestamp', timestamps)

    # Compute stats
    num_cov_cols = [col for col in df_combined.columns if col.startswith('NumSecCov_')]
    total_cov_cols = [col for col in df_combined.columns if col.startswith('NumSecCovTotal_')]

    df_combined['Min_NumSecCov'] = df_combined[num_cov_cols].min(axis=1).cummax()
    df_combined['Mean_NumSecCov'] = df_combined[num_cov_cols].mean(axis=1).cummax()
    df_combined['Min_NumSecCovTotal'] = df_combined[total_cov_cols].min(axis=1).cummax()
    df_combined['Mean_NumSecCovTotal'] = df_combined[total_cov_cols].mean(axis=1).cummax()

    # Final output
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
    print(f"✅ CSV written to {output_file} with valid timestamps and stats.")

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python3 csv_mounter.py file1.csv file2.csv file3.csv file4.csv file5.csv output.csv")
        sys.exit(1)

    file_list = sys.argv[1:6]
    output_file = sys.argv[6]
    process_csvs(file_list, output_file)
