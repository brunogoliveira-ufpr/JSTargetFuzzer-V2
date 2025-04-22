import os
import re
import pandas as pd
from datetime import datetime
from config import CODE_FILES_DIRECTORY, BATCH_SIZE
import json

# Regular expression to extract operations from Fuzzilli instruction lines in the format:
# Fuzzilli.Instruction(op: Fuzzilli.[OperationType], ...)
instruction_regex = re.compile(r'Fuzzilli\.Instruction\(op: Fuzzilli\.([A-Za-z]+),')

def load_cyclomatic_complexity():
    """
    Loads cyclomatic complexity data from a JSON file.
    """
    complexity_json_path = os.path.join(os.path.dirname(__file__), 'cyclomatic_complexity.json')
    with open(complexity_json_path, 'r', encoding='utf-8') as json_file:
        cyclomatic_data = json.load(json_file)
    return cyclomatic_data

def get_files_in_batches():
    """
    Retrieves all files from a specified directory and splits them into batches.
    """
    all_files = [os.path.join(CODE_FILES_DIRECTORY, f) for f in os.listdir(CODE_FILES_DIRECTORY) if f.endswith('.txt')]
    batches = [all_files[i:i + BATCH_SIZE] for i in range(0, len(all_files), BATCH_SIZE)]
    return batches

def process_file(file_path):
    """
    Processes a single file to extract Fuzzilli operations, their counts, cyclomatic complexity,
    and the file's modification date.
    """
    results = []  # Stores the results for each operation
    cyclomatic_data = load_cyclomatic_complexity()  # Load cyclomatic complexity data

    try:
        # Extract the 'weight' from the file name, using a regex to find patterns like "_weight_10.txt".
        weight_match = re.search(r'_weight_(\d+)\.txt', file_path)
        weight = int(weight_match.group(1)) if weight_match else 1

        # Get the modification date of the file
        mod_time = os.path.getmtime(file_path)
        mod_date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')

        # Read the file content into memory
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Extract all Fuzzilli operations using the regex
        operations = instruction_regex.findall(content)

        # Count the number of occurrences of each operation type
        operation_count = pd.Series(operations).value_counts().to_dict()

        for operation, qty in operation_count.items():
            # Get the cyclomatic complexity for the current operation (default to 0 if not found)
            complexity = cyclomatic_data.get(f"{operation}Generator", {}).get("cyclomatic_complexity", 1)
            
            # Append the result with operation name, quantity, weight, weighted complexity, and modification date
            results.append({
                'operation': operation,
                'qty': qty,
                'weight': weight,
                'cyclomatic_complexity': complexity * qty,  # Multiply complexity by number of occurrences
                'modification_date': mod_date  # Add modification date
            })
    except Exception as e:
        # Print an error message if the file cannot be processed
        print(f"Error processing file {file_path}: {e}")
    return results

def process_files_batch(file_paths):
    """
    Processes a batch of files.
    """
    batch_results = []  # To store results for all files in the batch
    for file_path in file_paths:
        # Process each file and extend the results into the batch results list
        batch_results.extend(process_file(file_path))
    return batch_results
