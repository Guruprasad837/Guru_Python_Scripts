import pandas as pd

# Load the first Excel file with all columns
file1 = pd.read_excel(r'C:\Users\mgg3kor\Desktop\Requirment Team\FORD\Cariad_radar_Image\SWLRR\expanded_Nonfunctional_dat.xlsx')

# Load the second Excel file which contains only ForeignID
file2 = pd.read_excel(r'C:\Users\mgg3kor\Desktop\Requirment Team\FORD\Cariad_radar_Image\Book1.xlsx', usecols=['ForeignID'])

# Convert ForeignID to string and strip whitespace in both DataFrames
file1['ForeignID'] = file1['ForeignID'].astype(str).str.strip()
file2['ForeignID'] = file2['ForeignID'].astype(str).str.strip()

# Merge the DataFrames based on ForeignID
merged = pd.merge(file1, file2, on='ForeignID', how='inner')

# Check if any matches were found
if merged.empty:
    print("No matches found.")
else:
    # Save the relevant columns to a new Excel file
    output_file_path = r'C:\Users\mgg3kor\Desktop\Requirment Team\FORD\Cariad_radar_Image\SWLRR\output.xlsx'
    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        merged.to_excel(writer, sheet_name='Merged', index=False)

    print(f'Results saved to {output_file_path}')
