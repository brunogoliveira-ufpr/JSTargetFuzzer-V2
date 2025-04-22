import re

def calculate_cyclomatic_complexity(instructions):
    num_instructions = len(instructions)
    num_decisions = sum(1 for instr in instructions if re.search(r'op: Fuzzilli\.(BeginIf|BeginElse|BeginSwitch|BeginSwitchCase|BeginFor|BeginWhileLoop|BeginDoWhileLoop|BeginTry|BeginCatch|BeginFinally|BeginWith)', instr))
    
    num_edges = num_instructions
    num_nodes = num_decisions
    
    complexity = num_edges - num_nodes + 2
    return complexity

def analyze_complexity(instructions, weight, complexity_metrics):
    complexity = calculate_cyclomatic_complexity(instructions)
    
    if weight not in complexity_metrics:
        complexity_metrics[weight] = []
    
    complexity_metrics[weight].append(complexity)
    
    return complexity_metrics

def average_complexity(complexity_metrics):
    average_metrics = {}
    for weight, complexities in complexity_metrics.items():
        average_metrics[weight] = sum(complexities) / len(complexities) if complexities else 0
    return average_metrics
