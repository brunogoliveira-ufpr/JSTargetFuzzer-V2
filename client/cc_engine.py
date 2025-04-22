import os
import lizard
import statistics

# Define the script directory as the base directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the name of the `.c` file to be analyzed
# file_name = "duk_api_stack.c"  # Replace with the correct file name
file_name = "ecma-function-object.c"  # Replace with the correct file name

# Generate the full path to the `.c` file
file_path = os.path.join(script_directory, file_name)

# Check if the file exists
if not os.path.exists(file_path):
    print(f"Error: File '{file_name}' not found in the script directory.")
else:
    # Analyze the file
    analysis = lizard.analyze_file(file_path)

    # Calculate the total number of functions and the cyclomatic complexity metrics
    total_functions = len(analysis.function_list)
    cc_values = [function.cyclomatic_complexity for function in analysis.function_list]
    total_cc = sum(cc_values)
    average_cc = statistics.mean(cc_values) if cc_values else 0
    std_cc = statistics.stdev(cc_values) if len(cc_values) > 1 else 0

    # Display the aggregated results
    print(f"File Analysis: {file_path}")
    print(f"Total number of functions: {total_functions}")
    print(f"Total Cyclomatic Complexity (CC): {total_cc}")
    print(f"Average Cyclomatic Complexity (CC): {average_cc:.2f}")
    print(f"Standard Deviation of Cyclomatic Complexity (CC): {std_cc:.2f}")
