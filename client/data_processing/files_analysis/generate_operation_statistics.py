import pandas as pd

def generate_operation_statistics(data):
    operation_types = set(op for counts in data['Operation Type Counts'] for op in counts.keys())
    
    operation_stats = {
        'Operation': [],
        '1 Count': [],
        '500 Count': [],
        '1 Mean': [],
        '500 Mean': [],
        '1 Lines': [],
        '500 Lines': []
    }
    
    for op in operation_types:
        operation_stats['Operation'].append(op)
        
        weight1_counts = [counts.get(op, 0) for counts, weight in zip(data['Operation Type Counts'], data['Weight']) if weight == 1]
        operation_stats['1 Count'].append(sum(weight1_counts))
        operation_stats['1 Mean'].append(sum(weight1_counts) / len(weight1_counts) if weight1_counts else 0)
        
        weight1_lines = [lines.get(op, 0) for lines, weight in zip(data['Lines Per Operation'], data['Weight']) if weight == 1]
        operation_stats['1 Lines'].append(sum(weight1_lines))
        
        weight500_counts = [counts.get(op, 0) for counts, weight in zip(data['Operation Type Counts'], data['Weight']) if weight == 1000]
        operation_stats['500 Count'].append(sum(weight500_counts))
        operation_stats['500 Mean'].append(sum(weight500_counts) / len(weight500_counts) if weight500_counts else 0)
        
        weight500_lines = [lines.get(op, 0) for lines, weight in zip(data['Lines Per Operation'], data['Weight']) if weight == 1000]
        operation_stats['500 Lines'].append(sum(weight500_lines))

    operation_stats_df = pd.DataFrame(operation_stats)
    return operation_stats_df
