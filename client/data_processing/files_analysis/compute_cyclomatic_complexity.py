import os
import re
import json

# Path to the Swift file
swift_file_path = os.path.join(os.path.dirname(__file__), 'CodeGenerators.swift')

# Regular expressions to match function definitions and control flow statements
function_regex = re.compile(
    r'(?:ValueGenerator|CodeGenerator|RecursiveValueGenerator|RecursiveCodeGenerator)\("([^"]+)"(?:, [^\)]*)?\) {([^}]+)}',
    re.DOTALL
)
control_flow_keywords = [
    'if', 'for', 'while', 'switch', 'case', 'default', 'catch', 'else', 'guard',
    'do', 'repeat', 'break', 'continue', 'throw', 'defer', 'return', 'try'
]

def compute_cyclomatic_complexity(function_body):
    """
    Compute the cyclomatic complexity and count control flow statements.
    """
    complexity = 1
    counts = {}
    for keyword in control_flow_keywords:
        pattern = r'\b' + keyword + r'\b'
        matches = re.findall(pattern, function_body)
        count = len(matches)
        if count > 0:
            counts[keyword] = count
            complexity += count
    return complexity, counts

def main():
    # Read the Swift file
    with open(swift_file_path, 'r', encoding='utf-8') as file:
        swift_code = file.read()

    # Find all functions
    functions = function_regex.findall(swift_code)

    # Dictionary to store the results
    complexity_dict = {}

    for func_name, func_body in functions:
        complexity, counts = compute_cyclomatic_complexity(func_body)
        complexity_dict[func_name] = {
            "cyclomatic_complexity": complexity,
            "control_flow_counts": counts
        }

    # Output JSON file
    output_file = os.path.join(os.path.dirname(__file__), 'cyclomatic_complexity.json')
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(complexity_dict, json_file, indent=4)

    print(f"Cyclomatic complexity computed for {len(complexity_dict)} functions.")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
