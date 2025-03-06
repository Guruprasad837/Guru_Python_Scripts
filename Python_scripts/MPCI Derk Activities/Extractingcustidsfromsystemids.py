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

# Extract multiple IDs starting from the beginning or after the dot, and ending before colon
def extract_multiple_ids(text):
    if pd.isna(text):  # Handle missing values
        return None
    text = str(text)  # Ensure the value is a string
    # Extract IDs between the beginning of the string (or after a dot) and the colon
    matches = re.findall(r'(\d+)(?=:)', text)  # Capture numbers before colon
    return matches if matches else None

# Apply the function to extract both IDs into a new column
df['Extracted ID'] = df['Guru'].apply(extract_multiple_ids)

# Explode the DataFrame to separate the extracted IDs into separate rows
df_exploded = df.explode('Extracted ID')

# Reset index
df_exploded.reset_index(drop=True, inplace=True)

# Save the processed DataFrame to a new file
df_exploded.to_excel(output_file_path, index=False)

# Display the modified DataFrame
print("\nModified DataFrame:")
print(df_exploded.head())

print(f"\nProcessed data saved to: {output_file_path}")
