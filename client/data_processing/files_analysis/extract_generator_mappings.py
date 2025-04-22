import os
import re
import json

# Path to the Swift file
swift_file_path = os.path.join(os.path.dirname(__file__), 'CodeGenerators.swift')

def extract_generator_mappings():
    # Read the Swift file
    with open(swift_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    generator_types = ['ValueGenerator', 'CodeGenerator', 'RecursiveValueGenerator', 'RecursiveCodeGenerator']
    generator_start_regex = re.compile(
        r'(' + '|'.join(generator_types) + r')\("([^"]+)"(?:, [^\)]*)?\)\s*\{'
    )

    operation_regex = re.compile(r'\bb\.(\w+)\(')

    operation_to_generator = {}

    in_generator = False
    brace_count = 0
    generator_name = ''
    generator_body = ''

    for line in lines:
        if not in_generator:
            match = generator_start_regex.match(line.strip())
            if match:
                in_generator = True
                brace_count = 1
                generator_type = match.group(1)
                generator_name = match.group(2)
                generator_body = ''
                # If there is code after the opening brace, include it
                remaining_line = line[line.find('{')+1:]
                generator_body += remaining_line
                # Check for opening and closing braces in the remaining_line
                brace_count += remaining_line.count('{')
                brace_count -= remaining_line.count('}')
        else:
            generator_body += line
            brace_count += line.count('{')
            brace_count -= line.count('}')
            if brace_count == 0:
                # We have reached the end of the generator
                in_generator = False
                # Now process the generator_body
                operations = operation_regex.findall(generator_body)
                for operation in operations:
                    operation = operation.lower()  # Normalize operation name
                    if operation not in operation_to_generator:
                        operation_to_generator[operation] = []
                    if generator_name not in operation_to_generator[operation]:
                        operation_to_generator[operation].append(generator_name)
                generator_name = ''
                generator_body = ''

    # Save the mapping to a JSON file
    mapping_file = os.path.join(os.path.dirname(__file__), 'operation_to_generator.json')
    with open(mapping_file, 'w', encoding='utf-8') as json_file:
        json.dump(operation_to_generator, json_file, indent=4)

    total_mappings = sum(len(v) for v in operation_to_generator.values())
    print(f"Extracted {total_mappings} operation to generator mappings.")
    print(f"Mapping saved to {mapping_file}")

if __name__ == "__main__":
    extract_generator_mappings()
