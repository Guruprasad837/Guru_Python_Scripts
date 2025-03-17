import pandas as pd

# Load the data (Replace 'data.xlsx' with your actual file name)
df = pd.read_excel(r"C:\Users\mgg3kor\Downloads\hiupi.xlsx")

# Extract the numeric part of PI (assuming format like "PI23.3")
df["PI_Numeric"] = df["PI"].str.extract(r'(\d+\.\d+)').astype(float)

# Get the rows where each ID has the highest PI value
df_max = df.loc[df.groupby("ID")["PI_Numeric"].idxmax()]

# Drop the helper column "PI_Numeric" before saving
df_max = df_max.drop(columns=["PI_Numeric"])

# Save the result to a new file
df_max.to_excel(r"C:\Users\mgg3kor\Downloads\MM.xlsx", index=False)

print("File saved as MM.xlsx")
