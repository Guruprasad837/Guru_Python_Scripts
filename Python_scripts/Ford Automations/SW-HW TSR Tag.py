import pandas as pd

# Load the two Excel files
file1 = pd.read_excel(r'C:\Users\mgg3kor\Desktop\Requirment Team\FORD\PI30\Sprint1\24hrsTask_07012024\FunctionalSafety\TSR Type.xlsx', usecols=['Legacy ID', 'Tags'])
file2 = pd.read_excel(r'C:\Users\mgg3kor\Downloads\group_tda_Tags.xlsx', usecols=['Legacy ID'])

merged = pd.merge(file2, file1, on='Legacy ID', how='left')
merged = merged.dropna(subset=['Legacy ID'])
merged['Legacy ID'] = merged['Legacy ID'].str.strip()
writer = pd.ExcelWriter(r'C:\Users\mgg3kor\Desktop\Requirment Team\FORD\PI29\PI29 Sprint6\TSR\outputfile.xlsx', engine='xlsxwriter')
merged[['Legacy ID', 'Tags']].to_excel(writer, sheet_name='Merged', index=False)
writer._save()
