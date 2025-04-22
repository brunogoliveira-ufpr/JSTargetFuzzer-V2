import re

def parse_swift_code_generators(swift_code):
    """
    Parse the Swift code to extract code generators.
    
    Parameters:
    swift_code (str): The Swift code as a string.
    
    Returns:
    dict: A dictionary where keys are generator names and values are generator definitions.
    """
    pattern = re.compile(r'(ValueGenerator|CodeGenerator|RecursiveCodeGenerator)\("(\w+)"\)\s*\{.*?\}', re.DOTALL)
    generators = {}

    for match in pattern.finditer(swift_code):
        generator_type = match.group(1)
        generator_name = match.group(2)
        generator_code = match.group(0)
        generators[generator_name] = generator_code

    defined_operations = set([match.group(2) for match in pattern.finditer(swift_code)])
    known_operations = set(generators.keys())
    not_found_operations = defined_operations - known_operations

    if not_found_operations:
        print("Operações não encontradas:", not_found_operations)

    for name, code in generators.items():
        print(f"Operation: {name}")
    
    return generators
