import os
import pandas as pd
 
def merge_excel_files(folder_path, out):
    # Initialize an empty list to hold DataFrames
    merged_data = []
   
    # Loop through each file in the folder
    for file in os.listdir(folder_path):
        if file.endswith('.xlsx'):
            file_path = os.path.join(folder_path, file)
            df = pd.read_excel(file_path)
            merged_data.append(df)
   
    # Concatenate all DataFrames in the list into one
    merged_data = pd.concat(merged_data, ignore_index=True)
   
    # Save the merged DataFrame to an Excel file
    out_path = os.path.join(folder_path, out)
    merged_data.to_excel(out_path, index=False)
 
if __name__ == "__main__":
    folder_path = r"C:\Users\mgg3kor\Downloads\MERGE"
    output_file = 'CusRS.xlsx'
    merge_excel_files(folder_path, output_file)