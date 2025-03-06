import pandas as pd
import re
import os

# Define the output directory
output_directory = r'C:\Users\mgg3kor\Desktop\Requirment Team\FORD\Cariad_radar_Image\trail'

# Load the initial Excel file
input_file_path = os.path.join(output_directory, r'C:\Users\mgg3kor\Desktop\Requirment Team\FORD\Cariad_radar_Image\SWLRR\Book1.xlsx')
df = pd.read_excel(input_file_path)
print("Original DataFrame:")
print(df.head())

# Define a function to extract numeric IDs
def extract_ids(requirement):
    if isinstance(requirement, str):
        functional_ids = re.findall(r'\[Functional: (\d+)\]', requirement)
        information_ids = re.findall(r'\[Information: (\d+)\]', requirement)
        non_functional_ids = re.findall(r'\[Non-functional: (\d+)\]', requirement)
        
        # Combine all IDs into a single list and convert to integers
        all_ids = list(map(int, functional_ids + information_ids + non_functional_ids))
        return all_ids
    else:
        return []

# Create a new column to store extracted IDs
df['IDs'] = df['Requirement'].apply(extract_ids)

# Filter out only the rows that have at least one ID
functional_data = df[df['IDs'].apply(lambda x: len(x) > 0)]

# Display the relevant data
print("\nFiltered Data with Extracted IDs:")
print(functional_data[['Requirement', 'IDs']])

# Save the extracted data to a new Excel file
extracted_file_path = os.path.join(output_directory, 'extracted_Functional.xlsx')
functional_data.to_excel(extracted_file_path, index=False)
print(f"\nExtracted functional data saved to: {extracted_file_path}")

# Load the extracted data to further process it
df_extracted = pd.read_excel(extracted_file_path)

# Clean up the Functional_IDs column and split the IDs
df_extracted['Functional_IDs'] = df_extracted['IDs'].astype(str)
df_extracted['Functional_IDs'] = df_extracted['Functional_IDs'].str.replace("'", "").str.strip()
df_extracted['Functional_IDs'] = df_extracted['Functional_IDs'].str.split(',')

# Explode the DataFrame to separate rows
df_exploded = df_extracted.explode('Functional_IDs')
df_exploded.reset_index(drop=True, inplace=True)

# Rename the column from Functional_IDs to ForeignID
df_exploded.rename(columns={'Functional_IDs': 'ForeignID'}, inplace=True)

# Clean ForeignID values in df_exploded
df_exploded['ForeignID'] = df_exploded['ForeignID'].astype(str).str.replace(r'[,\[\]]', '', regex=True).str.strip()

# Save the modified DataFrame to a new Excel file
expanded_file_path = os.path.join(output_directory, 'expanded_Nonfunctional_dat.xlsx')
df_exploded.to_excel(expanded_file_path, index=False)
print(f"\nExpanded data saved to: {expanded_file_path}")

# Load the ForeignID file
file2_path = os.path.join(output_directory, r'C:\Users\mgg3kor\Desktop\Requirment Team\FORD\Cariad_radar_Image\ff.xlsx')
file2 = pd.read_excel(file2_path, usecols=['ForeignID'])

# Clean ForeignID values in file2
file2['ForeignID'] = file2['ForeignID'].astype(str).str.replace(r'[,\[\]]', '', regex=True).str.strip()

# Merge the DataFrames based on ForeignID
merged = pd.merge(df_exploded, file2, on='ForeignID', how='inner')

# Check if any matches were found
if merged.empty:
    print("No matches found.")
else:
    # Remove unnecessary columns (if required)
    merged = merged.drop(columns=['Requirement', 'IDs'], errors='ignore')

    # Save the relevant columns to a new Excel file
    output_file_path = os.path.join(output_directory, 'output.xlsx')
    merged.to_excel(output_file_path, sheet_name='Merged', index=False)
    print(f'Results saved to {output_file_path}')
