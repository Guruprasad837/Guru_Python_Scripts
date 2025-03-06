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

# Function to extract only numbers with 6 or more digits before colons
def extract_ids_before_colon(text):
    if pd.isna(text):  # Handle missing values
        return None
    text = str(text)  # Ensure the value is a string
    matches = re.findall(r'(\d{6,})(?=[:])', text)  # Extract numbers with 6 or more digits before colons
    return matches if matches else None

# Apply function to extract numbers with 6 or more digits
df['Extracted IDs'] = df['Guru'].apply(extract_ids_before_colon)

# Explode to separate rows for each extracted ID
df_exploded = df.explode('Extracted IDs')

# Reset index
df_exploded.reset_index(drop=True, inplace=True)

# Save to new Excel file
df_exploded.to_excel(output_file_path, index=False)

# Display modified DataFrame
print("\nModified DataFrame:")
print(df_exploded.head())

print(f"\nProcessed data saved to: {output_file_path}")
