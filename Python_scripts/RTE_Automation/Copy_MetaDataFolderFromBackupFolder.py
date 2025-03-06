import shutil
import os

def copy_metadata(source_path, destination_path):
    try:
        # Check if the destination folder exists
        if os.path.exists(destination_path):
            metadata_folder_path = os.path.join(destination_path, '_metadata')
            # Check if the _metadata folder exists
            if os.path.exists(metadata_folder_path):
                # Remove the _metadata folder
                shutil.rmtree(metadata_folder_path)
                print(f"_metadata folder at '{metadata_folder_path}' removed.")

            # Move the source folder to the destination path
            shutil.move(source_path, destination_path)
            print(f"Folder '{source_path}' moved to '{destination_path}' successfully.")
        else:
            print(f"Destination path '{destination_path}' does not exist.")
    except FileNotFoundError:
        print(f"Error: Source folder '{source_path}' not found.")
    except shutil.Error as e:
        print(f"Error moving folder: {e}")

def main(dest_root_path,root_path,choice):
    #choice = input("Select 1 for primary 2 for secondary which you ran on BCT(For taking the _metadatafolder from Backup to Repo ): ")
    if choice not in ("1", "2"):
        print("Invalid choice. Please enter 1 or 2.")
        return

    source_path = os.path.join(root_path, f"Prj\\App\\Cubas_config\\Drv{'Pri' if choice == '1' else 'Sec'}Blade\\config\\Rte\\Rte\\generateforRte\\_metadata")
    destination_path = os.path.join(dest_root_path, f"Prj\\App\\Cubas_config\\Drv{'Pri' if choice == '1' else 'Sec'}Blade\\config\\Rte\\Rte\\generateforRte")

    copy_metadata(source_path, destination_path)