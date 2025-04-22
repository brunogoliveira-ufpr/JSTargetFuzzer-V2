import pandas as pd
import re

# Mapping operations to groups (with lists)
custom_op_group = {
    "Variables": [
        "DefineNamedVariable",
        "LoadNamedVariable",
        "Reassign",
        "StoreNamedVariable",
        "GetComputedProperty",
        "SetComputedProperty",
        "GetElement",
        "SetElement",
        "GetProperty",
        "SetProperty",
        "Update",
        "UpdateComputedProperty",
        "UpdateElement",
        "UpdateProperty",
        "UpdateSuperProperty",
        "DeleteProperty",
        "DeleteElement",
        "DeleteComputedProperty"
    ],
    "Loops": [
        "BeginForLoopBody",
        "BeginForLoopCondition",
        "BeginForLoopInitializer",
        "BeginForLoopAfterthought",
        "BeginForInLoop",
        "BeginForOfLoop",
        "BeginDoWhileLoopBody",
        "BeginDoWhileLoopHeader",
        "BeginWhileLoopBody",
        "BeginWhileLoopHeader",
        "BeginRepeatLoop",
        "EndForLoop",
        "EndForInLoop",
        "EndForOfLoop",
        "EndDoWhileLoop",
        "EndWhileLoop",
        "EndRepeatLoop",
        "LoopBreak",
        "LoopContinue"
    ],
    "Numeric Operations": [
        "BinaryOperation",
        "UnaryOperation",
        "Compare",
        "TernaryOperation",
        "Update",
        "TypeOf",
        "TestInstanceOf",
        "TestIn"
    ]
}

# Function to map operations to their respective groups
def map_operation_to_group(operation):
    for group, operations in custom_op_group.items():
        if operation in operations:
            return group
    return "Other"  # If the operation doesn't belong to any group

# Function to create a valid file name from the title
def create_valid_filename(title):
    # Replace spaces and special characters with underscores and remove invalid characters
    valid_filename = re.sub(r'[^\w\s-]', '', title).replace(' ', '_')
    return valid_filename

# Function to load, group, and display the CSV
def process_and_group_csv(file_path, weight_label, title):
    # Load the CSV
    df = pd.read_csv(file_path)

    # Map the operations to groups
    df['group'] = df['operation'].apply(map_operation_to_group)

    # Group by 2-hour block and group, aggregating values
    grouped_df = df.groupby(['2_hour_block', 'group']).agg({
        'sum_qty': 'sum',
        'total_complexity': 'sum',
        'file_count': 'sum',
        'avg_qty_by_weight': 'sum',
        'avg_complexity_by_weight': 'sum',
        'min_qty': 'min',
        'max_qty': 'max',
        'std_qty': 'std',
        'min_complexity': 'min',
        'max_complexity': 'max',
        'std_complexity': 'std'
    }).reset_index()

    output = []
    
    # Add title
    output.append(f"### {title}\n")

       
    for block in grouped_df['2_hour_block'].unique():
        output.append(f"Block {block}:\n")
        for group in ["Variables", "Loops", "Numeric Operations"]:
            if group in grouped_df['group'].values:
                block_df = grouped_df[(grouped_df['2_hour_block'] == block) & (grouped_df['group'] == group)]
                
                if not block_df.empty:
                    avg_qty_value = block_df['avg_qty_by_weight'].values[0]
                    min_qty_value = block_df['min_qty'].values[0]
                    max_qty_value = block_df['max_qty'].values[0]
                    std_qty_value = block_df['std_qty'].values[0]

                    avg_complexity_value = block_df['avg_complexity_by_weight'].values[0]
                    min_complexity = block_df['min_complexity'].values[0]
                    max_complexity = block_df['max_complexity'].values[0]
                    std_complexity = block_df['std_complexity'].values[0]
                    
                    # Add metrics to output
                    output.append(f"  {group}:\n")
                    output.append(f"    Avg Quantity: {avg_qty_value:.2f}\n")
                    output.append(f"    Min Quantity: {min_qty_value}\n")
                    output.append(f"    Max Quantity: {max_qty_value}\n")
                    output.append(f"    Std Dev Quantity: {std_qty_value:.2f}\n")
                    output.append(f"    Avg Cyclomatic Complexity: {avg_complexity_value:.2f}\n")
                    output.append(f"    Min Cyclomatic Complexity: {min_complexity}\n")
                    output.append(f"    Max Cyclomatic Complexity: {max_complexity}\n")
                    output.append(f"    Std Dev: {std_complexity:.2f}\n")

    # Display total cyclomatic complexity stats for each 2-hour block
    for block in grouped_df['2_hour_block'].unique():
        block_df = grouped_df[grouped_df['2_hour_block'] == block]
        total_avg_complexity = block_df['avg_complexity_by_weight'].sum()
        min_complexity_total = block_df['min_complexity'].min()
        max_complexity_total = block_df['max_complexity'].max()
        std_complexity_total = block_df['std_complexity'].sum()

        # Add total complexity stats to output
        output.append(f"\nBlock {block}:\n")
        output.append(f"  Total Cyclomatic Complexity (Sum): {total_avg_complexity:.2f}\n")
        output.append(f"  Avg Cyclomatic Complexity: {total_avg_complexity / len(block_df):.2f}\n")
        output.append(f"  Min Cyclomatic Complexity: {min_complexity_total}\n")
        output.append(f"  Max Cyclomatic Complexity: {max_complexity_total}\n")
        output.append(f"  Std Dev : {std_complexity_total:.2f}\n")

    # Create a valid file name from the title
    valid_filename = create_valid_filename(title)
    
    # Save output to a text file with the title as filename
    with open(f'{valid_filename}.txt', 'w') as f:
        f.writelines(output)

    return grouped_df

# Example usage
weight = 1000
file_path = f"/home/kali/JSTargetFuzzer-main/cli/cyclomatic/analysis_weight_{weight}_by_2_hour_blocks.csv"
title = f"Fuzzilli Duktape Weight {weight}"
filtered_df = process_and_group_csv(file_path, 1, title)
