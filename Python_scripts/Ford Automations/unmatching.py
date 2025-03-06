import pandas as pd

# Load the first Excel file with all columns
file1 = pd.read_excel(r'C:\Users\mgg3kor\Downloads\76 ID.xlsx')

# Load the second Excel file which contains only ForeignID
file2 = pd.read_excel(r'C:\Users\mgg3kor\Desktop\Requirment Team\FORD\Cariad_radar_Image\Hyd\lrr.xlsx', usecols=['ForeignID'])

# Convert ForeignID to string and strip whitespace in both DataFrames
file1['ForeignID'] = file1['ForeignID'].astype(str).str.strip()
file2['ForeignID'] = file2['ForeignID'].astype(str).str.strip()

# Merge the DataFrames based on ForeignID to find matches
merged = pd.merge(file1, file2, on='ForeignID', how='outer', indicator=True)

# Extract unmatched records
unmatched_file1 = merged[merged['_merge'] == 'left_only'][['ForeignID']]  # IDs only in file1
unmatched_file2 = merged[merged['_merge'] == 'right_only'][['ForeignID']]  # IDs only in file2

# Save the unmatched ForeignIDs to a new Excel file
output_unmatched_path = r'C:\Users\mgg3kor\Desktop\Requirment Team\FORD\Cariad_radar_Image\Hyd\output_unmatched.xlsx'
with pd.ExcelWriter(output_unmatched_path, engine='xlsxwriter') as writer:
    unmatched_file1.to_excel(writer, sheet_name='Unmatched in File1', index=False)
    unmatched_file2.to_excel(writer, sheet_name='Unmatched in File2', index=False)

print(f'Unmatched Foreign IDs saved to {output_unmatched_path}')
