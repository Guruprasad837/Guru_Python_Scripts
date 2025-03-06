import pandas as pd

# Prompt user for file paths
file_path = input("Enter the path to your input Excel file: ")
output_file_path = input("Enter the path to save the output Excel file: ")

# Load Excel file
df = pd.read_excel(file_path)

# Function to split by semicolon, clean up spaces, and filter only numbers
def split_and_filter_numbers(text):
    if pd.isna(text):  # Handle missing values
        return None
    return [item.strip() for item in str(text).split(";") if item.strip().isdigit()]

# Apply function to extract only numbers
df["Extracted Values"] = df["Guru"].apply(split_and_filter_numbers)

# Explode the list into separate rows
df_exploded = df.explode("Extracted Values").reset_index(drop=True)

# Save to new Excel file
df_exploded.to_excel(output_file_path, index=False)

print("\nModified DataFrame:")
print(df_exploded.head())

print(f"\nProcessed data saved to: {output_file_path}")
