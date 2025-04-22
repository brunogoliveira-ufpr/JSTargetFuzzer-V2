def translate_to_il(generators):
    """
    Translate Swift code generators to intermediate language (IL).
    
    Parameters:
    generators (dict): A dictionary where keys are generator names and values are generator definitions.
    
    Returns:
    dict: A dictionary where keys are generator names and values are IL representations.
    """
    il_instructions = {}

    for generator_name, generator_code in generators.items():
        # Here we perform a simple transformation to IL, for the sake of example
        # You can replace this with actual translation logic
        il_code = generator_code.replace('ValueGenerator', 'IL_Generator')
        il_instructions[generator_name] = il_code

    return il_instructions
