"""
Script Name: ARXML Modifier
Scope: Modify specific DTC paths in ARXML files.
Author: [mgg3kor]
Date: [02.20.2025]
Description: Python script designed to process and modify ARXML files by replacing 
specific patterns in diagnostic event paths. It extracts and updates path elements based on a predefined regex pattern.
"""


import re

# Example: Set the input and output file paths
# input_file = r"C:\Users\mgg3kor\Downloads\817D DrivingBladePrimary.arxml"
# output_file = r"C:\Users\mgg3kor\Downloads\output.arxml"

# Get file paths from the user
input_file = input("Enter the path of the input ARXML file (e.g., C:\\Users\\mgg3kor\\Downloads\\817D DrivingBladePrimary.arxml): ")
output_file = input("Enter the path of the output ARXML file (e.g., C:\\Users\\mgg3kor\\Downloads\\output.arxml): ")

with open(input_file, "r", encoding="utf-8") as file:
    arxml_content = file.read()

# Regex pattern to match required cases
pattern = re.compile(r'(DIAGNOSTIC-EVENT">/DCAXCaller/DTC/DTC/(BOSCH_[^/]+|RB_UC[^/]+|DEM_[^/]+))/([^/\s<]+)')

last_elements = []
second_last_elements = []

def replace_last_element(match):
    second_last = match.group(2)
    last = match.group(3)
    
    last_elements.append(last)
    second_last_elements.append(second_last)
    
    return f'{match.group(1)}/{second_last}'

modified_content = re.sub(pattern, replace_last_element, arxml_content)

for last, second_last in zip(last_elements, second_last_elements):
    modified_content = re.sub(rf'{re.escape(last)}', second_last, modified_content)

# Save the modified ARXML file
with open(output_file, "w", encoding="utf-8") as file:
    file.write(modified_content)

print(f"Replacement completed. Check {output_file}")
