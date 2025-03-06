import pandas as pd
RB=1
SB=0
def Get_IDS():
    df = pd.read_excel(r'C:\Users\mgg3kor\Desktop\Requirment Team\ANn\AAA\ID_Input.xlsx')
    def extract_last_number(id_str):
        parts = id_str.rsplit('_', 1)  
        last_part = parts[-1]
        if last_part.isdigit():
            return int(last_part)
        else:
            return None  
 
    df['Last_Number'] = df['IDs'].apply(extract_last_number)

    output_file_path = r'C:\Users\mgg3kor\Desktop\Requirment Team\ANn\AAA\ID_Output.xlsx'
    df.to_excel(output_file_path, index=False)
 
    print("Output saved to Excel file:", output_file_path)

def Copy_Attributes(counter):
    df_original = pd.read_excel(r'C:\Users\mgg3kor\Desktop\Requirment Team\ANn\AAA\Input file (1).xlsx')
    if (counter == 1):
         columns_to_copy = ['Module_Path', 'Object_ID_from_Original', 'RB_Comment']
         df_new = df_original[columns_to_copy].copy()
         df_new['Attributes'] = 'RB_Comment'
         df_new.to_excel(r'C:\Users\mgg3kor\Desktop\Requirment Team\ANn\AAA\Attribute_output.xlsx')
         print("RB_Comment Data has been successfully copied and saved to new_file.xlsx.")
    else:
         
         columns_to_copy = ['Module_Path', 'Object_ID_from_Original', 'Status_Bosch']
         df_new = df_original[columns_to_copy].copy()
         df_new['Attributes'] = 'Status_Bosch'
         df_new.to_excel(r'C:\Users\mgg3kor\Desktop\Requirment Team\ANn\AAA\RB_Attribute_output.xlsx')
         print("Status_Bosch Data has been successfully copied and saved to new_file.xlsx.")
         
     
def Replace_IDs():
         
    df_last_number = pd.read_excel(r'C:\Users\mgg3kor\Desktop\Requirment Team\ANn\AAA\ID_Output.xlsx')
    df_target = pd.read_excel(r'C:\Users\mgg3kor\Desktop\Requirment Team\ANn\AAA\RB_Attribute_output.xlsx')
    df_last_number.rename(columns={'Last_Number': 'Object_ID_from_Original'}, inplace=True)
    df_merged = df_target.merge(df_last_number[['Object_ID_from_Original']], left_index=True, right_index=True)
    df_target['Object_ID_from_Original'] = df_merged['Object_ID_from_Original_y']
    df_target.to_excel(r'C:\Users\mgg3kor\Desktop\Requirment Team\ANn\AAA\Status_bosch_output.xlsx', index=False)
    print("IDs Replaced Successfully")


def RB_Comments():
       
        Get_IDS()
        Copy_Attributes(SB)
        Replace_IDs()
def Status_Bosch():
       Get_IDS()
       Copy_Attributes(RB)


if __name__ == '__main__':
     RB_Comments()
     Status_Bosch()
        
