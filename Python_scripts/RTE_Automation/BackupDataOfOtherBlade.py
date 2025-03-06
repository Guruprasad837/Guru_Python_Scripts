import shutil
import os
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

def main(dest_root_path,root_path,choice):
    # Determine the target subfolder based on user input
    #choice = input("Select 1 for primary and 2 for secondary which you ran On BCT: ")

    if choice == '2':
        source_path1 = os.path.join(root_path, 'Prj\App\Cubas_config\DrvPriBlade\config\Rte\Rte')
        destination_path1 = os.path.join(dest_root_path, 'Prj\App\Cubas_config\DrvPriBlade\config\Rte\Rte')
    elif choice == '1':
        source_path1 = os.path.join(root_path, 'Prj\App\Cubas_config\DrvSecBlade\config\Rte\Rte')
        destination_path1 = os.path.join(dest_root_path, 'Prj\App\Cubas_config\DrvSecBlade\config\Rte\Rte')
    else:
        print("Invalid choice. No action taken.")
        return

    # Specify the folders to move from main repository
    folders_to_move = ['backupForRte', 'generateforRte']
    source_paths = [os.path.join(source_path1, folder_name) for folder_name in folders_to_move]
    destination_path = os.path.join(source_path1, destination_path1)

    # Overwrite the folders in the destination path with the latest version
    overwrite_folders_with_latest(source_paths, destination_path)

