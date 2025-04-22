# data_processing/files_analysis/categorize_operations.py
import pandas as pd
from .categories import OPERATION_CATEGORIES, CATEGORY_DESCRIPTIONS

def categorize_operations(operation_stats):
    categorized_stats = {
        'Category': [], 
        'Operation': [], 
        '1 Count': [], 
        '1000 Count': [], 
        '1 Mean': [], 
        '1000 Mean': [], 
        '1 Lines': [], 
        '1000 Lines': [], 
        'Category Description': []
    }
    unknown_operations = []

    for op in operation_stats['Operation']:
        category = OPERATION_CATEGORIES.get(op, 'Unknown')
        description = CATEGORY_DESCRIPTIONS.get(category, 'No description available.')
        
        if category == 'Unknown':
            unknown_operations.append(op)
        
        categorized_stats['Category'].append(category)
        categorized_stats['Category Description'].append(description)
        categorized_stats['Operation'].append(op)
        categorized_stats['1 Count'].append(operation_stats.loc[operation_stats['Operation'] == op, '1 Count'].values[0])
        categorized_stats['1000 Count'].append(operation_stats.loc[operation_stats['Operation'] == op, '1000 Count'].values[0])
        categorized_stats['1 Mean'].append(operation_stats.loc[operation_stats['Operation'] == op, '1 Mean'].values[0])
        categorized_stats['1000 Mean'].append(operation_stats.loc[operation_stats['Operation'] == op, '1000 Mean'].values[0])
        categorized_stats['1 Lines'].append(operation_stats.loc[operation_stats['Operation'] == op, '1 Lines'].values[0])
        categorized_stats['1000 Lines'].append(operation_stats.loc[operation_stats['Operation'] == op, '1000 Lines'].values[0])
    
    categorized_df = pd.DataFrame(categorized_stats)
    return categorized_df, unknown_operations
