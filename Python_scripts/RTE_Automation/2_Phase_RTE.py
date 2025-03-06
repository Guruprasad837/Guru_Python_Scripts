import os
import shutil


def backup_and_remove_folders(root_folder, backup_path):
    # Define folders and files to backup and remove
    folders_to_backup_remove = ['backupForRte', 'generateForRte']
    files_to_remove = ['Com_Model_Export.arxml', 'Xfrm_Model_Export.arxml']
    
    # Create or clean up the backup folder
    if os.path.exists(backup_path):
        shutil.rmtree(backup_path)
    os.makedirs(backup_path, exist_ok=True)

    # Traverse through the root folder
    for root, dirs, files in os.walk(root_folder):
        # Backup and remove specified folders
        for folder_name in folders_to_backup_remove:
            folder_path = os.path.join(root, folder_name)
            if os.path.exists(folder_path):
                backup_folder_path = os.path.join(backup_path, os.path.relpath(folder_path, root_folder))
                shutil.copytree(folder_path, backup_folder_path)
                shutil.rmtree(folder_path)
                print(f"Backed up and removed folder: {folder_path}")

        # Remove specified files
        for file_name in files:
            if file_name in files_to_remove:
                file_path = os.path.join(root, file_name)
                if not file_path.startswith(backup_path):
                    os.remove(file_path)
                    print(f"Removed file: {file_path}")



# Prompt the user to specify the MPCI repository and Backup_folder

Mpci_envac = input("Enter the path of your MPCI repository(Mpci_envac): ")
Backup_folder = input("Enter the path of your backup folder: ")
# Prompt the user to specify the blade choice
choice = input("Enter 1 for DrvPriBlade or 2 for DrvSecBlade: ")

# Perform backup and removal

if choice in ['1', '2']:
    blade_name = 'DrvPriBlade' if choice == '1' else 'DrvSecBlade'
else:
    print("Invalid choice. Please enter 1 or 2.")

backup_and_remove_folders(Mpci_envac, Backup_folder)



#Mpci_envac = r'C:\Users\mgg3kor\Desktop\Requirment Team\Python Scripts\RTE_Automation\mpci_envac'
#Backup_folder = r"C:\Users\mgg3kor\Desktop\Requirment Team\Python Scripts\RTE_Automation\Backups"



