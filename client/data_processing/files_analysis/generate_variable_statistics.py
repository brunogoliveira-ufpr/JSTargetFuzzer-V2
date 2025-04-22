# data_processing/files_analysis/generate_variable_statistics.py
import pandas as pd

def generate_variable_statistics(data):
    variable_stats = {'Operation': [], 'Weight': [], 'Variable': [], 'Count': []}
    
    for i, op_counts in enumerate(data['Variable Type Counts']):
        weight = data['Weight'][i]
        for op, vars_dict in op_counts.items():
            for var, count in vars_dict.items():
                variable_stats['Operation'].append(op)
                variable_stats['Weight'].append(weight)
                variable_stats['Variable'].append(var)
                variable_stats['Count'].append(count)

    variable_stats_df = pd.DataFrame(variable_stats)
    return variable_stats_df
