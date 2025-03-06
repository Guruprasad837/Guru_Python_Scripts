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

# Function to extract the number after the decimal before the colon
def extract_second_part(text):
    if pd.isna(text):  # Handle missing values
        return None
    text = str(text)  # Ensure it's a string

    # Extract number after decimal (before colon)
    matches = re.findall(r'\d{6,}\.(\d+)(?=[:])', text)
    
    return matches if matches else None

# Function to extract the middle text (between colon `:` and `{`)
def extract_middle_text(text):
    if pd.isna(text):  # Handle missing values
        return None
    text = str(text)

    # Extract everything after the first colon and before `{`
    match = re.search(r':\s*([^{}]+)', text)

    return match.group(1).strip() if match else None

# Apply functions to extract values
df['Extracted IDs'] = df['Guru'].apply(extract_second_part)  # Extract numbers after decimal
df['Extracted Middle Text'] = df['Guru'].apply(extract_middle_text)  # Extract text between `:` and `{`

# Explode to separate rows for each extracted ID
df_exploded = df.explode('Extracted IDs')

# Fill empty "Extracted IDs" cells with "Extracted Middle Text" (Fixed for Pandas 3.0)
df_exploded['Extracted IDs'] = df_exploded['Extracted IDs'].fillna(df_exploded['Extracted Middle Text'])

# Reset index
df_exploded.reset_index(drop=True, inplace=True)

# Save to new Excel file
df_exploded.to_excel(output_file_path, index=False)

# Display modified DataFrame
print("\nModified DataFrame:")
print(df_exploded.head())

print(f"\nProcessed data saved to: {output_file_path}")
