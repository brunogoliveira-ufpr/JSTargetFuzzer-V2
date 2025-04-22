# data_processing/compare_weights_analysis.py
import os
import re
import pandas as pd
import streamlit as st
from ..files_analysis.categories import OPERATION_CATEGORIES  # Importar categorias de operações

def parse_operations(file_content):
    operations = re.findall(r'Fuzzilli\.Instruction\(op: Fuzzilli\.(\w+)', file_content)
    return operations

def count_operations_and_variables(file_content):
    operations = re.findall(r'Fuzzilli\.Instruction\(op: Fuzzilli\.(\w+), inouts_: \[([^\]]+)\]', file_content)
    operation_counts = {}
    variable_counts = {}
    total_variables = 0

    for op, vars in operations:
        if op in operation_counts:
            operation_counts[op] += 1
        else:
            operation_counts[op] = 1
        
        vars_list = vars.split(', ')
        for var in vars_list:
            if var in variable_counts:
                variable_counts[var] += 1
            else:
                variable_counts[var] = 1
        
        total_variables += len(vars_list)

    return operation_counts, total_variables, variable_counts

def cyclomatic_complexity(file_content):
    # Simplified cyclomatic complexity calculation based on number of branches and loops
    branches_loops = len(re.findall(r'if|else|while|for|case|switch', file_content))
    return branches_loops + 1

def count_lines_per_operation(operation_counts):
    # Each operation corresponds to one line
    lines_per_operation = {op: count for op, count in operation_counts.items()}
    return lines_per_operation

def categorize_operations(operation_stats):
    categorized_stats = {'Category': [], 'Operation': [], '1 Count': [], '500 Count': [], '1 Mean': [], '500 Mean': [], '1 Lines': [], '500 Lines': []}
    unknown_operations = []

    for op in operation_stats['Operation']:
        category = OPERATION_CATEGORIES.get(op, 'Unknown')
        if category == 'Unknown':
            unknown_operations.append(op)
        
        categorized_stats['Category'].append(category)
        categorized_stats['Operation'].append(op)
        categorized_stats['1 Count'].append(operation_stats['1 Count'][operation_stats['Operation'].index(op)])
        categorized_stats['500 Count'].append(operation_stats['500 Count'][operation_stats['Operation'].index(op)])
        categorized_stats['1 Mean'].append(operation_stats['1 Mean'][operation_stats['Operation'].index(op)])
        categorized_stats['500 Mean'].append(operation_stats['500 Mean'][operation_stats['Operation'].index(op)])
        categorized_stats['1 Lines'].append(operation_stats['1 Lines'][operation_stats['Operation'].index(op)])
        categorized_stats['500 Lines'].append(operation_stats['500 Lines'][operation_stats['Operation'].index(op)])
    
    categorized_df = pd.DataFrame(categorized_stats)
    return categorized_df, unknown_operations

def save_unknown_operations(unknown_operations, directory):
    filepath = os.path.join(directory, 'unknown_operations.txt')
    with open(filepath, 'w') as file:
        for op in unknown_operations:
            file.write(f"{op}\n")

def compare_weights_analysis(directory):
    weight1_files = [f for f in os.listdir(directory) if 'weight1' in f]
    weight500_files = [f for f in os.listdir(directory) if 'weight500' in f]

    data = {
        'File': [],
        'Weight': [],
        'Operations Count': [],
        'Variables Count': [],
        'Cyclomatic Complexity': [],
        'Operation Type Counts': [],
        'Variable Type Counts': [],
        'Lines Per Operation': []
    }

    for weight1_file in weight1_files:
        file_path = os.path.join(directory, weight1_file)
        with open(file_path, 'r') as file:
            content = file.read()
            operation_counts, total_variables, variable_counts = count_operations_and_variables(content)
            complexity = cyclomatic_complexity(content)
            lines_per_operation = count_lines_per_operation(operation_counts)
            
            data['File'].append(weight1_file)
            data['Weight'].append(1)
            data['Operations Count'].append(sum(operation_counts.values()))
            data['Variables Count'].append(total_variables)
            data['Cyclomatic Complexity'].append(complexity)
            data['Operation Type Counts'].append(operation_counts)
            data['Variable Type Counts'].append(variable_counts)
            data['Lines Per Operation'].append(lines_per_operation)

    for weight500_file in weight500_files:
        file_path = os.path.join(directory, weight500_file)
        with open(file_path, 'r') as file:
            content = file.read()
            operation_counts, total_variables, variable_counts = count_operations_and_variables(content)
            complexity = cyclomatic_complexity(content)
            lines_per_operation = count_lines_per_operation(operation_counts)
            
            data['File'].append(weight500_file)
            data['Weight'].append(500)
            data['Operations Count'].append(sum(operation_counts.values()))
            data['Variables Count'].append(total_variables)
            data['Cyclomatic Complexity'].append(complexity)
            data['Operation Type Counts'].append(operation_counts)
            data['Variable Type Counts'].append(variable_counts)
            data['Lines Per Operation'].append(lines_per_operation)

    df = pd.DataFrame(data)
    
    st.header("Detailed File Data")
    st.write(df)

    # Detailed statistics for operations
    operation_types = set(op for counts in data['Operation Type Counts'] for op in counts.keys())
    
    # Create a DataFrame for operation statistics
    operation_stats = {'Operation': [], '1 Count': [], '500 Count': [], '1 Mean': [], '500 Mean': [], '1 Lines': [], '500 Lines': []}
    
    for op in operation_types:
        operation_stats['Operation'].append(op)
        
        # Count and mean for weight 1
        weight1_counts = [counts.get(op, 0) for counts, weight in zip(data['Operation Type Counts'], data['Weight']) if weight == 1]
        operation_stats['1 Count'].append(sum(weight1_counts))
        operation_stats['1 Mean'].append(sum(weight1_counts) / len(weight1_counts) if weight1_counts else 0)
        
        # Lines for weight 1
        weight1_lines = [lines.get(op, 0) for lines, weight in zip(data['Lines Per Operation'], data['Weight']) if weight == 1]
        operation_stats['1 Lines'].append(sum(weight1_lines))
        
        # Count and mean for weight 500
        weight500_counts = [counts.get(op, 0) for counts, weight in zip(data['Operation Type Counts'], data['Weight']) if weight == 500]
        operation_stats['500 Count'].append(sum(weight500_counts))
        operation_stats['500 Mean'].append(sum(weight500_counts) / len(weight500_counts) if weight500_counts else 0)
        
        # Lines for weight 500
        weight500_lines = [lines.get(op, 0) for lines, weight in zip(data['Lines Per Operation'], data['Weight']) if weight == 500]
        operation_stats['500 Lines'].append(sum(weight500_lines))

    operation_stats_df = pd.DataFrame(operation_stats)
    
    st.header("Operation Statistics")
    st.write(operation_stats_df)

    # Categorize and group operations
    categorized_df, unknown_operations = categorize_operations(operation_stats)
    
    grouped_df = categorized_df.groupby('Category').agg(
        {'1 Count': 'sum', '500 Count': 'sum', '1 Mean': 'mean', '500 Mean': 'mean', '1 Lines': 'sum', '500 Lines': 'sum'}
    ).reset_index()
    
    st.header("Grouped Operation Statistics by Category")
    st.write(grouped_df)

    if unknown_operations:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        save_unknown_operations(unknown_operations, script_directory)
        st.header("Unknown Operations")
        st.write(unknown_operations)

    # Summary statistics
    overall_summary = {
        'Metric': [
            'Total Programs',
            'Programs with Weight 1',
            'Programs with Weight 500',
            'Average Operations Count',
            'Average Variables Count',
            'Average Cyclomatic Complexity'
        ],
        'Value': [
            len(df),
            len(df[df['Weight'] == 1]),
            len(df[df['Weight'] == 500]),
            df['Operations Count'].mean(),
            df['Variables Count'].mean(),
            df['Cyclomatic Complexity'].mean()
        ]
    }
    
    overall_summary_df = pd.DataFrame(overall_summary)
    
    st.header("Overall Summary Statistics")
    st.write(overall_summary_df)
