# data_processing/files_analysis/cyclomatic_complexity.py
import re

def cyclomatic_complexity(file_content):
    branches_loops = len(re.findall(r'if|else|while|for|case|switch', file_content))
    return branches_loops + 1
