import subprocess
import os

script_dir = r"C:\MyScripts\Guru_Python_Scripts\Python_scripts\Automated Email Downloaded RTC Problem Tickets"

files_to_run = [
    "MPCI_SW_SYS_OlderProblems_3Months_COM.py",
    "MPCI_SW_SYS_OlderProblems_3Months_DRB.py",
    "MPCI_SW_SYS_OlderProblems_3Months_Diag.py",
    "MPCI_SW_SYS_OlderProblems_3Months_MaaS.py",
    "MPCI_SW_SYS_OlderProblems_3Months_OPMM.py",
    "MPCI_SW_SYS_OlderProblems_3Months_Safety.py",
    "MPCI_SW_SYS_OlderProblems_3Months_Security.py"
]

processes = []
for file in files_to_run:
    file_path = os.path.join(script_dir, file)
    if os.path.exists(file_path):
        processes.append(subprocess.Popen(["python", file_path]))
    else:
        print(f"Error: {file} not found in {script_dir}")

# Wait for all processes to complete
for process in processes:
    process.wait()
