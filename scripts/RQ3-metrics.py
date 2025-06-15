# -*- coding: utf-8 -*-
import os
import lizard
import re
from statistics import mean, stdev

# Regular expression to match loop constructs
loop_pattern = re.compile(r'\b(for|while|do)\b')

def count_loops_in_file(file_path):
    """Count the number of loops (for, while, do) in the file."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        loops = loop_pattern.findall(content)
        return len(loops)

def analyze_js_files(files):
    cyclomatic_complexities = []
    variable_counts = []
    operation_counts = []
    loop_counts = []

    for file_path in files:
        analysis = lizard.analyze_file(file_path)

        file_cyclomatic = 0
        file_variables = 0
        file_operations = 0

        for function in analysis.function_list:
            file_cyclomatic += function.cyclomatic_complexity
            file_operations += function.token_count
            file_variables += len(function.parameters)

        file_loops = count_loops_in_file(file_path)

        cyclomatic_complexities.append(file_cyclomatic)
        variable_counts.append(file_variables)
        operation_counts.append(file_operations)
        loop_counts.append(file_loops)

    return {
        "avg_cyclomatic": mean(cyclomatic_complexities) if cyclomatic_complexities else 0,
        "min_cyclomatic": min(cyclomatic_complexities) if cyclomatic_complexities else 0,
        "max_cyclomatic": max(cyclomatic_complexities) if cyclomatic_complexities else 0,
        "stddev_cyclomatic": stdev(cyclomatic_complexities) if len(cyclomatic_complexities) > 1 else 0,

        "avg_variables": mean(variable_counts) if variable_counts else 0,
        "min_variables": min(variable_counts) if variable_counts else 0,
        "max_variables": max(variable_counts) if variable_counts else 0,
        "stddev_variables": stdev(variable_counts) if len(variable_counts) > 1 else 0,

        "avg_operations": mean(operation_counts) if operation_counts else 0,
        "min_operations": min(operation_counts) if operation_counts else 0,
        "max_operations": max(operation_counts) if operation_counts else 0,
        "stddev_operations": stdev(operation_counts) if len(operation_counts) > 1 else 0,

        "avg_loops": mean(loop_counts) if loop_counts else 0,
        "min_loops": min(loop_counts) if loop_counts else 0,
        "max_loops": max(loop_counts) if loop_counts else 0,
        "stddev_loops": stdev(loop_counts) if len(loop_counts) > 1 else 0
    }

def print_results(results, label):
    print(f"Results for {label}:")
    print(f"  Cyclomatic Complexity: Avg = {results['avg_cyclomatic']:.2f}, Min = {results['min_cyclomatic']}, Max = {results['max_cyclomatic']}, Std Dev = {results['stddev_cyclomatic']:.2f}")
    print(f"  Number of Variables:   Avg = {results['avg_variables']:.2f}, Min = {results['min_variables']}, Max = {results['max_variables']}, Std Dev = {results['stddev_variables']:.2f}")
    print(f"  Number of Operations:  Avg = {results['avg_operations']:.2f}, Min = {results['min_operations']}, Max = {results['max_operations']}, Std Dev = {results['stddev_operations']:.2f}")
    print(f"  Number of Loops:       Avg = {results['avg_loops']:.2f}, Min = {results['min_loops']}, Max = {results['max_loops']}, Std Dev = {results['stddev_loops']:.2f}")
    print()

def analyze_js_directory(directory):
    all_files = []
    weight_1_files = []
    weight_1000_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.js'):
                file_path = os.path.join(root, file)
                all_files.append(file_path)

                if file.endswith('weight_1.js'):
                    weight_1_files.append(file_path)
                elif file.endswith('weight_1000.js'):
                    weight_1000_files.append(file_path)

    print_results(analyze_js_files(all_files), "all files")
    print_results(analyze_js_files(weight_1_files), "files with weight_1")
    print_results(analyze_js_files(weight_1000_files), "files with weight_1000")

if __name__ == "__main__":
    js_directory = "/home/kali/PhD/JSTargetFuzzer-Jerry/crashes-jerry-full/crashes"
    analyze_js_directory(js_directory)
