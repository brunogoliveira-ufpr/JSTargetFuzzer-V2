# data_processing/files_analysis/count_operations_and_variables.py
import re

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
