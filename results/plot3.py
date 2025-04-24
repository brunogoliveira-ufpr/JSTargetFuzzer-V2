import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Define input CSV files
input_files = {
    'ChakraCore': './ChakraCore-JSTargetFuzzer.csv',
    'Duktape': './Duktape-JSTargetFuzzer.csv',
    'JavaScriptCore': './JavaScriptCore-JSTargetFuzzer.csv',
    'Jerryscript': './Jerryscript-JSTargetFuzzer.csv',
}

fuzzilli_files = {
    'ChakraCore': './ChakraCore-Fuzzilli.csv',
    'Duktape': './Duktape-Fuzzilli.csv',
    'JavaScriptCore': './JavaScriptCore-Fuzzilli.csv',
    'Jerryscript': './Jerryscript-Fuzzilli.csv',
}

# Directory for plots
output_dir = "./"
os.makedirs(output_dir, exist_ok=True)

for engine in input_files:
    df1 = pd.read_csv(input_files[engine])
    df2 = pd.read_csv(fuzzilli_files[engine])

    # Remove non-numeric rows (like 'TOTAL') and ensure numeric
    for df in [df1, df2]:
        df.dropna(subset=['HitCount', 'UniqueHitCount'], inplace=True)
        df = df[~df['HitCount'].astype(str).str.contains("[a-zA-Z]", na=False)]
        df['HitCount'] = pd.to_numeric(df['HitCount'], errors='coerce')
        df['UniqueHitCount'] = pd.to_numeric(df['UniqueHitCount'], errors='coerce')
        df.dropna(inplace=True)

    # Apply logarithmic transformation to HitCount
    df1['HitCount'] = np.log10(df1['HitCount'].replace(0, np.nan)).fillna(0)
    df2['HitCount'] = np.log10(df2['HitCount'].replace(0, np.nan)).fillna(0)

    length = min(len(df1), len(df2))
    elapsed = list(range(length))

    # Plot HitCount (log-transformed)
    plt.figure(figsize=(10, 5), facecolor='white')
    plt.plot(elapsed, df1['HitCount'][:length], label='JSTargetFuzzer', marker='o')
    plt.plot(elapsed, df2['HitCount'][:length], label='Fuzzilli', marker='o')
    plt.xlabel('ElapsedTime (Hours)')
    plt.ylabel('Log10(HitCount)')
    plt.xticks([0, 360, 720, 1080, 1440], ['0h', '6h', '12h', '18h', '24h'])
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{engine}-HitCount-LOG.png"))
    plt.close()

    # Plot UniqueHitCount (raw)
    plt.figure(figsize=(10, 5), facecolor='white')
    plt.plot(elapsed, df1['UniqueHitCount'][:length], label='JSTargetFuzzer', marker='o')
    plt.plot(elapsed, df2['UniqueHitCount'][:length], label='Fuzzilli', marker='o')
    plt.xlabel('ElapsedTime (Hours)')
    plt.ylabel('UniqueHitCount')
    plt.xticks([0, 360, 720, 1080, 1440], ['0h', '6h', '12h', '18h', '24h'])
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{engine}-UniqueHitCount.png"))
    plt.close()
