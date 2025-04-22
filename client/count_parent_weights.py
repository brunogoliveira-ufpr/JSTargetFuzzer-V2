import pandas as pd
import os

# Global weight variables
PARENT_WEIGHTS = [1.00, 50.00, 1000.00]  # Weights to analyze for parents
CHILD_WEIGHTS = [1.00, 50.00, 1000.00]   # Weights to analyze for children

def count_weights():
    # Name of the CSV file in the same directory as the script
    file_name = "parent_child_map.csv"
    file_path = os.path.join(os.getcwd(), file_name)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_name}' was not found in the current directory: {os.getcwd()}")
        return
    
    # Load the CSV file with explicit delimiter and column names
    column_names = ["Parent ID", "Parent Weight", "Child ID", "Child Weight"]
    df = pd.read_csv(file_path, delimiter=",", names=column_names, skiprows=1)
    
    # Display column names for debugging
    print("Column names:", df.columns.tolist())
    
    # Analysis
    results = {}
    for parent_weight in PARENT_WEIGHTS:
        # Filter rows for parents with the current weight
        parent_rows = df[df["Parent Weight"] == parent_weight]
        
        # Count children by weight for this parent weight
        child_counts = {}
        for child_weight in CHILD_WEIGHTS:
            child_counts[child_weight] = len(parent_rows[parent_rows["Child Weight"] == child_weight])
        
        # Store results
        results[parent_weight] = child_counts
    
    # Display results
    print("\nDetailed Analysis Results:")
    for parent_weight, child_counts in results.items():
        print(f"Parent Weight {parent_weight}:")
        for child_weight, count in child_counts.items():
            print(f"  Children with Weight {child_weight}: {count}")

if __name__ == "__main__":
    count_weights()
