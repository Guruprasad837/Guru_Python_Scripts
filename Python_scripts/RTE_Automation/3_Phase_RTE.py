
import os
import shutil
# Define paths
Mpci_envac = input("Enter the path of your MPCI repository(Mpci_envac): ")
Backup_folder = input("Enter the path of your backup folder: ")
choice = input("Select 1 for primary and 2 for secondary which you ran On BCT: ")
def delete_folder_in_root(folder_name,root_path):
    folder_path = os.path.join(root_path, folder_name)

    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_name}' deleted successfully.")
    except FileNotFoundError:
        print(f"Error: Folder '{folder_name}' not found.")
    except OSError as e:
        print(f"Error deleting folder '{folder_name}': {e}")
def overwrite_folders_with_latest(source_paths, destination_path):
    try:
        # Iterate over the source folders
        for source_path in source_paths:
            folder_name = os.path.basename(source_path)
            destination_folder_path = os.path.join(destination_path, folder_name)

            # Check if the destination folder exists
            if os.path.exists(destination_folder_path):
                # Remove the destination folder to overwrite it with the source folder
                shutil.rmtree(destination_folder_path)
                print(f"Existed '{folder_name}' removed.")

            # Move the source folder to the destination path
            shutil.move(source_path, destination_path)
            print(f"Folder '{source_path}' moved to '{destination_path}' successfully.")
    except Exception as e:
        print(f"Error moving folders: {e}")

def main(choice):
    # Example usage:
    folder_name_to_delete = 'backupForBsw'
    delete_folder_in_root(folder_name_to_delete,Mpci_envac)

    # Determine the target subfolder based on user input
    #choice = input("Select 1 for primary and 2 for secondary which you ran On BCT: ")

    if choice == '1':
        target_subfolder = 'Prj\App\Cubas_config\DrvPriBlade\config\Rte\Rte'
    elif choice == '2':
        target_subfolder = 'Prj\App\Cubas_config\DrvSecBlade\config\Rte\Rte'
    else:
        print("Invalid choice. No action taken.")
        return

    # Specify the folders to move from main repository
    folders_to_move = ['backupForRte', 'generateforRte']

    # Construct source and destination paths for main repository folders
    source_paths = [os.path.join(Mpci_envac, folder_name) for folder_name in folders_to_move]
    destination_path = os.path.join(Mpci_envac, target_subfolder)

    # Overwrite the folders in the destination path with the latest version
    overwrite_folders_with_latest(source_paths, destination_path)

if __name__ == "__main__":

    main(choice)
import Copy_MetaDataFolderFromBackupFolder
Copy_MetaDataFolderFromBackupFolder.main(Mpci_envac,Backup_folder,choice)
import BackupDataOfOtherBlade
BackupDataOfOtherBlade.main(Mpci_envac,Backup_folder,choice)