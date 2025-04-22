def count_lines_per_operation(content, operation_counts):
    """
    Count the number of lines per operation in the given content.

    Parameters:
    content (str): The content of the file.
    operation_counts (dict): A dictionary where keys are operation names and values are their counts.

    Returns:
    dict: A dictionary where keys are operation names and values are line counts.
    """
    lines_per_operation = {op: 0 for op in operation_counts.keys()}
    lines = content.split('\n')

    for line in lines:
        for operation in lines_per_operation.keys():
            if operation in line:
                lines_per_operation[operation] += 1

    # Ensure the line count is multiplied by the operation count
    for op in lines_per_operation.keys():
        lines_per_operation[op] *= operation_counts[op]

    return lines_per_operation
