import pandas as pd
import re
from openpyxl import load_workbook

# Load the Excel file (replace 'input_file.xlsx' with the path to your actual file)
input_file = r'C:\Users\mgg3kor\Desktop\Requirment Team\FORD\Cariad_radar_Image\Pyhton Scripts\radar\UpdatedFile.xlsx'
output_file = r'C:\Users\mgg3kor\Desktop\Requirment Team\FORD\Cariad_radar_Image\Pyhton Scripts\radar\output_file.xlsx'

# Load the workbook and select the active sheet
wb = load_workbook(input_file)
sheet = wb.active

# Initialize lists to store the cleaned requirements, types, and their corresponding IDs
cleaned_requirements = []
requirement_types = []
requirement_ids = []

# Iterate over each cell in the 'Req' column (assuming 'Req' is in the first column)
for cell in sheet['A']:  # Adjust if 'Req' column is not 'A'
    row_text = str(cell.value)

    # Split the cell content by the specified patterns
    requirements = re.split(r'(?=\[Functional:|\[Non-functional:|\[Information:)', row_text)
    
    for req in requirements:
        if req.strip():  # Ignore empty splits
            # Extract the type and ID from the tag if they exist
            match = re.search(r'\[(Functional|Non-functional|Information): (\d+)\]', req)
            if match:
                # Extract type and ID
                req_type = match.group(1)
                req_id = match.group(2)
                
                # Remove the tag from the requirement text
                cleaned_req = re.sub(r'\[(Functional|Non-functional|Information): \d+\]', '', req).strip()
                
                # Add the cleaned requirement, type, and ID
                cleaned_requirements.append(cleaned_req)
                requirement_types.append(req_type)
                requirement_ids.append(req_id)
            else:
                # If no type/ID is found, append the original requirement without modifications and mark type/ID as None
                cleaned_requirements.append(req.strip())
                requirement_types.append(None)
                requirement_ids.append(None)

# Create a new DataFrame from the cleaned requirements, types, and IDs
new_df = pd.DataFrame({
    'Requirement': cleaned_requirements,
    'Type': requirement_types,
    'ID': requirement_ids
})

# Save the new DataFrame to an Excel file
new_df.to_excel(output_file, index=False)
print(f"Split requirements with types and IDs saved to {output_file}")
