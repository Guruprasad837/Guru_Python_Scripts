import pandas as pd

# Load your Excel file
file_path = r'C:\Users\mgg3kor\Downloads\IS1 RT3 SW Requirements_DurgaGuruSwapnil.xlsx'
df = pd.read_excel(file_path)

# Display the original DataFrame
print("Original DataFrame:")
print(df)

# Clean up the 'System req id' column and split into lists
df['System req id'] = df['System req id'].astype(str).str.replace("'", "").str.strip()  # Remove unwanted characters
df['System req id'] = df['System req id'].str.split(',')  # Split the IDs into lists using ','

# Explode the DataFrame to create separate rows for each ID
df_exploded = df.explode('System req id')

# Reset the index to ensure it is sequential
df_exploded.reset_index(drop=True, inplace=True)

# Display the modified DataFrame
print("\nModified DataFrame:")
print(df_exploded)

# Save the modified DataFrame to a new Excel file
expanded_file_path = r'C:\Users\mgg3kor\Desktop\Requirment Team\FORD\Cariad_radar_Image\SWLRR\expanded_Nonfunctional_dat.xlsx'
df_exploded.to_excel(expanded_file_path, index=False)

print(f"\nExpanded data saved to: {expanded_file_path}")
