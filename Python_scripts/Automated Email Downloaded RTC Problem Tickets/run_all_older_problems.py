import subprocess

files_to_run = [
    "MPCI_SW_SYS_OlderProblems_3Months_COM.py",
    "MPCI_SW_SYS_OlderProblems_3Months_DRB.py",
    "MPCI_SW_SYS_OlderProblems_3Months_Diag.py",
    "MPCI_SW_SYS_OlderProblems_3Months_MaaS.py",
    "MPCI_SW_SYS_OlderProblems_3Months_OPMM.py",
    "MPCI_SW_SYS_OlderProblems_3Months_Safety.py",
    "MPCI_SW_SYS_OlderProblems_3Months_Security.py"
]

processes = [subprocess.Popen(["python", file]) for file in files_to_run]

# Wait for all processes to complete
for process in processes:
    process.wait()
