import os
import shutil

def copy_arxml_to_backup(blade_path):
    backup_for_rte_path = os.path.join(blade_path, 'config', 'Rte', 'Rte', 'backupForRte')
    rte_adapter_path = os.path.join(blade_path, 'config', 'Rte', 'Rte', 'rte_adapter')

    if not os.path.exists(rte_adapter_path):
        print(f"Error: The rte_adapter folder doesn't exist at {rte_adapter_path}")
        return

    if not os.path.exists(backup_for_rte_path):
        os.makedirs(backup_for_rte_path)

    arxml_file = os.path.join(backup_for_rte_path, 'System_EcuExtr.arxml')
    if os.path.exists(arxml_file):
        shutil.copy(arxml_file, rte_adapter_path)
        print("System_EcuExtr.arxml copied successfully to rte_adapter folder.")
    else:
        print("Error: System_EcuExtr.arxml file not found in backupForRte folder.")



# Prompt the user to specify the MPCI repository and Backup_folder

Mpci_envac = input("Enter the path of your MPCI repository(Mpci_envac): ")
#Backup_folder = input("Enter the path of your backup folder: ")
# Prompt the user to specify the blade choice
choice = input("Enter 1 for DrvPriBlade or 2 for DrvSecBlade: ")

# Perform backup and removal

if choice in ['1', '2']:
    blade_name = 'DrvPriBlade' if choice == '1' else 'DrvSecBlade'
    blade_path = os.path.join(Mpci_envac, 'Prj\App\Cubas_config', blade_name)
    copy_arxml_to_backup(blade_path)
else:
    print("Invalid choice. Please enter 1 or 2.")




