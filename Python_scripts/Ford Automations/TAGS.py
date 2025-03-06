import pandas as pd

# Load the two Excel files
file1 = pd.read_excel(r'C:\Users\mgg3kor\Downloads\tags.xlsx', usecols=['Legacy ID', 'Tags'])
file2 = pd.read_excel(r'C:\Users\mgg3kor\Downloads\tagsfile.xlsx', usecols=['Legacy ID'])

merged = pd.merge(file2, file1, on='Legacy ID', how='left')
merged = merged.dropna(subset=['Legacy ID'])
merged['Legacy ID'] = merged['Legacy ID'].str.strip()
writer = pd.ExcelWriter(r'C:\Users\mgg3kor\Downloads\output.xlsx', engine='xlsxwriter')
merged[['Legacy ID', 'Tags']].to_excel(writer, sheet_name='Merged', index=False)
writer._save()
