import pandas as pd
import re

# Prompt user for file paths
file_path = input("Enter the path to your input Excel file: ")
output_file_path = input("Enter the path to save the output Excel file: ")

# Load Excel file
df = pd.read_excel(file_path)

# Ensure the column exists
column_name = 'Guru'  # Change if your column has a different name
if column_name not in df.columns:
    raise ValueError(f"Column '{column_name}' not found in the Excel file.")

# Function to extract all numbers after "/"
def extract_ids_after_slash(text):
    if pd.isna(text):
        return None
    return re.findall(r'/(\d+)', str(text))  # Extract all numbers after "/"

# Apply function to extract IDs
df['Extracted IDs'] = df[column_name].apply(extract_ids_after_slash)

# Explode to create separate rows for each extracted ID
df_exploded = df.explode('Extracted IDs')

# Reset index
df_exploded.reset_index(drop=True, inplace=True)

# Save results to a new Excel file (keeping all columns)
df_exploded.to_excel(output_file_path, index=False)

print(f"Processed data saved to: {output_file_path}")
