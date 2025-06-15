import pandas as pd
import matplotlib.pyplot as plt
import os

input_files = {
    'ChakraCore': './ChakraCore-JSTargetFuzzer.csv',
    'Duktape': './Duktape-JSTargetFuzzer.csv',
    'JavaScriptCore': './JavaScriptCore-JSTargetFuzzer.csv',
    'Jerryscript': './Jerryscript-JSTargetFuzzer.csv',
}

color_map = {
    'ChakraCore':    '#1f77b4',
    'Duktape':       '#ff7f0e',
    'JavaScriptCore':'#2ca02c',
    'Jerryscript':   '#d62728',
}

output_dir = "./"
os.makedirs(output_dir, exist_ok=True)

plt.figure(figsize=(10, 5))
for engine in input_files:
    df = pd.read_csv(input_files[engine])
    df.dropna(subset=['HitCount'], inplace=True)
    df = df[~df['HitCount'].astype(str).str.contains("[a-zA-Z]", na=False)]
    df['HitCount'] = pd.to_numeric(df['HitCount'], errors='coerce')
    df.dropna(inplace=True)

    length = len(df)
    elapsed = list(range(length))

    plt.plot(elapsed, df['HitCount'], label=engine, color=color_map[engine], linewidth=1.2)

plt.xlabel('Elapsed Time (Minutes)')
plt.ylabel('HitCount')
plt.yticks([])

time_intervals = [0, length // 4, length // 2, 3 * length // 4, length - 1]
time_labels = ['0m', '30m', '60m', '90m', '120m']
plt.xticks(time_intervals, time_labels)

plt.grid(True, axis='y', linestyle='--', alpha=0.6)
plt.legend(ncol=2, fontsize=12)  # Increased font size
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "AllEngines-HitCount-Full.png"))
plt.close()

plt.figure(figsize=(10, 5))
for engine in input_files:
    df = pd.read_csv(input_files[engine])
    df.dropna(subset=['UniqueHitCount'], inplace=True)
    df = df[~df['UniqueHitCount'].astype(str).str.contains("[a-zA-Z]", na=False)]
    df['UniqueHitCount'] = pd.to_numeric(df['UniqueHitCount'], errors='coerce')
    df.dropna(inplace=True)

    length = len(df)
    elapsed = list(range(length))

    plt.plot(elapsed, df['UniqueHitCount'], label=engine, color=color_map[engine], linewidth=1.2)

plt.xlabel('Elapsed Time (Minutes)')
plt.ylabel('UniqueHitCount')
plt.yticks([])
plt.xticks(time_intervals, time_labels)
plt.grid(True, axis='y', linestyle='--', alpha=0.6)
plt.legend(ncol=2, fontsize=12)  # Increased font size
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "AllEngines-UniqueHitCount-Full.png"))
plt.close()
