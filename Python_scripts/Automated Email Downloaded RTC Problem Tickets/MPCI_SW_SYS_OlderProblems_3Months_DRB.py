import os
import time
import pandas as pd
import win32com.client
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

# Define the Downloads folder path
download_path = os.path.expanduser("~\\Downloads")

# Define expected filename pattern
expected_filename_keyword = "MPCI_SW_SYS_OlderProblems_3Months_DRB"

# Function to delete old CSV files
def delete_specific_csv(download_folder, filename_keyword):
    for file in os.listdir(download_folder):
        if file.endswith(".csv") and filename_keyword in file:
            os.remove(os.path.join(download_folder, file))
            print(f"Deleted old file: {file}")

delete_specific_csv(download_path, expected_filename_keyword)

# Set up WebDriver
driver = webdriver.Chrome()

# RTC Query URL
rtc_url = "https://rb-alm-14-p.de.bosch.com/ccm/web/projects/CentralComputingRack%20(CCM)#action=com.ibm.team.workitem.runSavedQuery&id=_xJUzsvFDEe-LqNoB04ZrZg"

# Open RTC and download report
driver.get(rtc_url)
driver.implicitly_wait(10)
download_button = driver.find_element(By.ID, 'jazz_ui_toolbar_Button_1')  # Adjust as needed
download_button.click()
time.sleep(10)
driver.quit()

# Function to get latest CSV file
def get_latest_csv(download_folder, filename_keyword):
    files = [os.path.join(download_folder, f) for f in os.listdir(download_folder) if f.endswith(".csv") and filename_keyword in f]
    return max(files, key=os.path.getctime) if files else None

latest_csv_file = get_latest_csv(download_path, expected_filename_keyword)

if latest_csv_file:
    file_size = os.path.getsize(latest_csv_file)
    if file_size <= 1024:
        print(f"File {latest_csv_file} is {file_size} bytes (≤ 1KB). Email will not be sent.")
    else:
        # Load CSV
        df = pd.read_csv(latest_csv_file, encoding="utf-16", delimiter="\t")

        # Ensure required columns exist
        required_columns = ["Id", "Summary", "Creation Date", "Exclude"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = ""  # Fill missing columns with empty values

        today = datetime.today()

         # Enhanced date parsing
        def convert_to_days(date_str):
            if pd.isna(date_str):
                return "Unknown"
            formats = [
                "%b %d, %Y, %I:%M %p",    # Oct 3, 2024, 1:21 PM
                "%b %d, %Y %I:%M %p",     # Apr 22, 2024 11:30 AM
                "%m/%d/%Y %I:%M:%S %p",   # 04/22/2024 11:30:00 AM
                "%Y-%m-%d %H:%M:%S",      # 2024-04-22 11:30:00
                "%d.%m.%Y %H:%M"          # 22.04.2024 11:30
            ]
            for fmt in formats:
                try:
                    return (today - datetime.strptime(date_str.strip(), fmt)).days
                except ValueError:
                    continue
            print(f"Unrecognized date format: {date_str}")
            return "Unknown"

        df["Days Ago"] = df["Creation Date"].apply(convert_to_days)

        # Function to apply colors correctly for Outlook rendering
        def color_days_ago(days, exclude):
            if str(exclude).strip().lower() == "yes":
                return f"<td>{days}</td>"  # No color formatting

            if isinstance(days, int):
                if days > 100:
                    return f'<td style="background-color: red; color: white; font-weight: bold;">{days}</td>'
                elif days > 90:
                    return f'<td style="background-color: orange; color: black; font-weight: bold;">{days}</td>'

            return f"<td>{days}</td>"

        # HTML Table Styling with Gray Header
        html_table = """
        <style>
            table { border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; }
            th, td { border: 1px solid black; padding: 8px; text-align: left; }
            th { background-color: gray; color: white; }  /* Changed from Green to Gray */
        </style>
        <table>
            <tr>
                <th>ID</th>
                <th>Summary</th>
                <th>Days Ago</th>
            </tr>
        """

        for _, row in df.iterrows():
            id_val = row["Id"]
            summary = row["Summary"]
            exclude_flag = row["Exclude"]
            days_ago_html = color_days_ago(row["Days Ago"], exclude_flag)

            rtc_ticket_url = f"https://rb-alm-14-p.de.bosch.com/ccm/web/projects/CentralComputingRack%20(CCM)#action=com.ibm.team.workitem.viewWorkItem&id={id_val}"
            id_link = f'<td><a href="{rtc_ticket_url}" target="_blank" style="color: blue; font-weight: bold;">{id_val}</a></td>'

            html_table += f"<tr>{id_link}<td>{summary}</td>{days_ago_html}</tr>"

        html_table += "</table>"

        # Outlook Email Setup
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)

        #mail.To = "guruprasad.mangali@in.bosch.com"
        mail.To = "spai.aiswarya@in.bosch.com"
        mail.CC = "sathyan.krishnamoorthy@in.bosch.com; Manickam.Chokkalingam@in.bosch.com; NateshKumar.Kalasetty@in.bosch.com"
        mail.Subject = "[Automated] RTC Report: DRB Problem Tickets Older Than 3 Months"

        # Email Body with Table
        mail.HTMLBody = f"""
        <p>Hi Aiswarya,</p>

        <p>Please find attached the RTC report containing problem tickets that are older than 3 months. 
        You can also check the latest status through the live RTC query mentioned in the link below.</p>

        <p>🔗 <b><a href="{rtc_url}">RTC Query - DRB Problem Tickets Older Than 3 Months</a></b></p>

        <p>Here is a summary of the extracted data:</p>
        {html_table}

        <p>Best regards,<br>MPCI Automation</p>
        """

        mail.Attachments.Add(latest_csv_file)

        mail.Send()
        print(f"Email sent successfully with attachment: {latest_csv_file}")
else:
    print("No matching CSV file found in Downloads.")
