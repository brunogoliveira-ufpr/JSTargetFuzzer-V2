import os
import pandas as pd

def generate_detailed_file_data(directory, weight1_files, weight1000_files, count_operations_and_variables, cyclomatic_complexity, count_lines_per_operation):
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

    def process_file(file_name, weight):
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r') as file:
            content = file.read()
            operation_counts, total_variables, variable_counts = count_operations_and_variables(content)
            complexity = cyclomatic_complexity(content)
            lines_per_operation = count_lines_per_operation(content, operation_counts)
            
            data['File'].append(file_name)
            data['Weight'].append(weight)
            data['Operations Count'].append(sum(operation_counts.values()))
            data['Variables Count'].append(total_variables)
            data['Cyclomatic Complexity'].append(complexity)
            data['Operation Type Counts'].append(operation_counts)
            data['Variable Type Counts'].append(variable_counts)
            data['Lines Per Operation'].append(lines_per_operation)

    for weight1_file in weight1_files:
        process_file(weight1_file, 1)

    for weight1000_file in weight1000_files:
        process_file(weight1000_file, 1000)

    detailed_file_data_df = pd.DataFrame(data)
    return detailed_file_data_df
