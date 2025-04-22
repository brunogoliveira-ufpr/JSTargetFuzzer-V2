import re
from .fuzzilli_il import get_operation_mapping
def extract_instructions(content):
    pattern = re.compile(r'Fuzzilli\.Instruction\(op: [^\)]+\)')
    instructions = pattern.findall(content)
    return instructions

def analyze_instructions(instructions):
    analysis = {
        'total_instructions': len(instructions),
        'operation_counts': {},
        'variables_defined': set(),
        'variables_used': set()
    }
    
    for instruction in instructions:
        op_match = re.search(r'op: Fuzzilli\.([A-Za-z]+)', instruction)
        if op_match:
            operation = op_match.group(1)
            if operation not in analysis['operation_counts']:
                analysis['operation_counts'][operation] = 0
            analysis['operation_counts'][operation] += 1
        
        var_match = re.findall(r'v\d+', instruction)
        if var_match:
            analysis['variables_defined'].add(var_match[0])
            analysis['variables_used'].update(var_match[1:])

    analysis['variables_defined'] = list(analysis['variables_defined'])
    analysis['variables_used'] = list(analysis['variables_used'])
    
    return analysis

def translate_to_js(instructions):
    js_code = []
    var_mapping = {}
    var_counter = 0
    
    operation_mapping = get_operation_mapping()
    
    for instruction in instructions:
        op_match = re.search(r'op: Fuzzilli\.([A-Za-z]+)', instruction)
        var_match = re.findall(r'v\d+', instruction)
        
        if op_match and var_match:
            operation = op_match.group(1)
            inputs = var_match[1:]
            output = var_match[0]
            
            if output not in var_mapping:
                var_mapping[output] = f"v{var_counter}"
                var_counter += 1
            for var in inputs:
                if var not in var_mapping:
                    var_mapping[var] = f"v{var_counter}"
                    var_counter += 1
            
            js_var_output = var_mapping[output]
            js_var_inputs = [var_mapping[var] for var in inputs]
            
            if operation in operation_mapping:
                if operation in [
                    'BeginFor', 'BeginPlainFunction', 'BeginObjectLiteral', 
                    'BeginObjectLiteralMethod', 'BeginClassDefinition', 
                    'BeginClassInstanceSetter', 'BeginClassPrivateStaticMethod', 
                    'BeginConstructor'
                ]:
                    js_code.append(operation_mapping[operation](js_var_output, js_var_inputs))
                    js_code.append("  // Body of the operation")
                elif operation in [
                    'EndFor', 'EndPlainFunction', 'EndObjectLiteral', 
                    'EndObjectLiteralMethod', 'EndClassDefinition', 
                    'EndClassInstanceSetter', 'EndClassPrivateStaticMethod', 
                    'EndConstructor'
                ]:
                    js_code.append(operation_mapping[operation](js_var_output, js_var_inputs))
                else:
                    js_code.append(operation_mapping[operation](js_var_output, js_var_inputs))
            else:
                js_code.append(f"// Unhandled operation: {operation}")
    
    return "\n".join(js_code)

def count_lines_of_code(js_code):
    """
    Count the number of lines of code in the generated JavaScript code.
    """
    return len(js_code.split("\n"))
