import os
import time
import win32com.client
from selenium import webdriver
from selenium.webdriver.common.by import By

# Define the Downloads folder path
download_path = os.path.expanduser("~\\Downloads")

# Define expected filename pattern (Adjust based on actual downloaded file name)
expected_filename_keyword = "MPCI_SW_SYS_OlderProblems_3Months_OPMM"

# Function to delete only relevant CSV files
def delete_specific_csv(download_folder, filename_keyword):
    for file in os.listdir(download_folder):
        if file.endswith(".csv") and filename_keyword in file:
            os.remove(os.path.join(download_folder, file))
            print(f"Deleted old file: {file}")

# Delete only specific CSV file before downloading a new one
delete_specific_csv(download_path, expected_filename_keyword)

# Set up WebDriver
driver = webdriver.Chrome()

# Define the RTC query for problem tickets older than 3 months
rtc_url = "https://rb-alm-14-p.de.bosch.com/ccm/web/projects/CentralComputingRack%20(CCM)#action=com.ibm.team.workitem.runSavedQuery&id=_ahnnAvFDEe-LqNoB04ZrZg"

# Open the RTC URL
driver.get(rtc_url)

# Wait for page elements to load
driver.implicitly_wait(10)

# Locate and click the 'Download as Spreadsheet' button
download_button = driver.find_element(By.ID, 'jazz_ui_toolbar_Button_1')  # Replace with actual ID
download_button.click()

# Wait for the file to download
time.sleep(10)

# Close the browser
driver.quit()

# Function to get the latest downloaded CSV file related to the RTC report
def get_latest_csv(download_folder, filename_keyword):
    files = [os.path.join(download_folder, f) for f in os.listdir(download_folder) if f.endswith(".csv") and filename_keyword in f]
    return max(files, key=os.path.getctime) if files else None

# Get the latest specific CSV file
latest_csv_file = get_latest_csv(download_path, expected_filename_keyword)

if latest_csv_file:
    file_size = os.path.getsize(latest_csv_file)  # Get file size in bytes
    if file_size <= 1024:  # Check if file size is ≤ 1KB
        print(f"File {latest_csv_file} is {file_size} bytes (≤ 1KB). Email will not be sent.")
    else:
        # Open Outlook
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)  # Create a new email

        # Configure email details
        #mail.To ="Guruprasad.Mangali@in.bosch.com"
        mail.To = "Kavya.Rajkumar@in.bosch.com"
        mail.CC = "Pavitra.NV@in.bosch.com; Manickam.Chokkalingam@in.bosch.com; NateshKumar.Kalasetty@in.bosch.com"
        mail.Subject = "[Automated] RTC Report: OPMM Problem Tickets Older Than 3 Months"

        # Updated Email Body
        mail.Body = f"""Hi Kavya,

Please find attached the RTC report containing problem tickets that are older than 3 months. 
You can also check the latest status through the live RTC query mentioned in the link below.  

🔗 **[RTC Query - OPMM Problem Tickets Older Than 3 Months]( {rtc_url} )**  

Best regards,  
Guruprasad"""

        # Attach the downloaded CSV file
        mail.Attachments.Add(latest_csv_file)

        # Send the email
        mail.Send()
        print(f"Email sent successfully with attachment: {latest_csv_file}")

