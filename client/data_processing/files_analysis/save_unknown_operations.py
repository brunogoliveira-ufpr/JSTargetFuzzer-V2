# data_processing/files_analysis/save_unknown_operations.py
import os

def save_unknown_operations(unknown_operations, directory):
    filepath = os.path.join(directory, 'unknown_operations.txt')
    with open(filepath, 'w') as file:
        for op in unknown_operations:
            file.write(f"{op}\n")
