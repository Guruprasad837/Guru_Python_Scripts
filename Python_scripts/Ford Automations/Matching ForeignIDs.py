import pandas as pd

# Define the paths to your Excel files
file1_path = r'C:\Users\mgg3kor\Pictures\new module.xlsx'  # Please add customer file(export all attributes ForeignID',  'Responsibility', 'State_Bosch_pe', 'Comment_Bosch_pe', 'Bosch_Internal', 'Comment_OEM_Bosch_pe', 'State_OEM_Bosch_pe',  'ID', 'Type')
file2_path = r'C:\Users\mgg3kor\Pictures\oldmodukl.xlsx'  # Please add draft file (export only ForeignID)

# Read the Excel files into DataFrames
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

# Ensure the ForeignID and cForeignID columns are in the same format
df1['ForeignID'] = df1['ForeignID'].astype(str)
df2['ForeignID'] = df2['ForeignID'].astype(str)  # Adjust if this is the correct column in df2

# Fetch matching ForeignIDs
matched_ids = df2['ForeignID'].unique()
matched_df = df1[df1['ForeignID'].isin(matched_ids)]

# Keep the desired columns from df1, including ForeignID
desired_columns = [
    'ForeignID',  # Include the ForeignID column
    'Responsibility', 
    'State_Bosch_pe', 
    'Comment_Bosch_pe', 
    'Bosch_Internal', 
    'Comment_OEM_Bosch_pe', 
    'State_OEM_Bosch_pe', 
    'ID', 
    'Foreign_ID',
    'Type'
]

# Filter the matched DataFrame to include only the desired columns
matched_df = matched_df[desired_columns]

# Define the output path for the results
output_path = r'C:\Users\mgg3kor\Pictures\matched_results.xlsx'  # Path for output file
matched_df.to_excel(output_path, index=False)

print("Matching ForeignIDs have been fetched and saved to", output_path)
