import pandas as pd
import re

# Prompt the user to enter the input and output file paths
file_path = input("Enter the path to your input Excel file (e.g., C:\\Users\\your_name\\Documents\\file.xlsx): ")
output_file_path = input("Enter the path to save the output Excel file (e.g., C:\\Users\\your_name\\Documents\\output.xlsx): ")

# Load your Excel file
df = pd.read_excel(file_path)

# Display original DataFrame
print("Original DataFrame:")
print(df.head())

# Function to extract all numbers before each colon
def extract_starting_numbers(text):
    if pd.isna(text):  # Handle missing values
        return None
    text = str(text)  # Ensure it's a string

    # Find all numbers before each colon
    matches = re.findall(r'(\d+):', text)
    
    return matches if matches else None

# Apply function to extract the starting numbers
df['Extracted IDs'] = df['Guru'].apply(extract_starting_numbers)

# Explode the list into separate rows
df_exploded = df.explode('Extracted IDs').reset_index(drop=True)

# Reset index
df_exploded.reset_index(drop=True, inplace=True)

# Save to new Excel file
df_exploded.to_excel(output_file_path, index=False)

# Display modified DataFrame
print("\nModified DataFrame:")
print(df_exploded.head())

print(f"\nProcessed data saved to: {output_file_path}")
