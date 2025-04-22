# data_processing/files_analysis/generate_overall_summary.py
import pandas as pd

def generate_overall_summary(df):
    overall_summary = {
        'Metric': [
            'Total Programs',
            'Programs with Weight 1',
            'Programs with Weight 1000',
            'Average Operations Count',
            'Average Variables Count',
            'Average Cyclomatic Complexity',
            'Average Operations Count Weight 1',
            'Average Variables Count Weight 1',
            'Average Cyclomatic Complexity Weight 1',
            'Average Operations Count Weight 1000',
            'Average Variables Count Weight 1000',
            'Average Cyclomatic Complexity Weight 1000'
        ],
        'Value': [
            len(df),
            len(df[df['Weight'] == 1]),
            len(df[df['Weight'] == 1000]),
            df['Operations Count'].mean(),
            df['Variables Count'].mean(),
            df['Cyclomatic Complexity'].mean(),
            df[df['Weight'] == 1]['Operations Count'].mean(),
            df[df['Weight'] == 1]['Variables Count'].mean(),
            df[df['Weight'] == 1]['Cyclomatic Complexity'].mean(),
            df[df['Weight'] == 1000]['Operations Count'].mean(),
            df[df['Weight'] == 1000]['Variables Count'].mean(),
            df[df['Weight'] == 1000]['Cyclomatic Complexity'].mean()
        ]
    }
    overall_summary_df = pd.DataFrame(overall_summary)
    return overall_summary_df
