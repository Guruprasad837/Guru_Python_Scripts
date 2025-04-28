import os
import time
import pandas as pd
import win32com.client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


# Define the Downloads folder path
download_path = os.path.expanduser("~\\Downloads")
today_date = datetime.today().strftime('%B %d, %Y')

# Team details: (Team Title, Query URL, Filename Keyword)
teams_info = [
    ("COM Team", "https://rb-alm-14-p.de.bosch.com/ccm/web/projects/CentralComputingRack%20(CCM)#action=com.ibm.team.workitem.runSavedQuery&id=__6_tsvFCEe-LqNoB04ZrZg", "MPCI_SW_SYS_OlderProblems_3Months_COM"),
    ("Diag Team", "https://rb-alm-14-p.de.bosch.com/ccm/web/projects/CentralComputingRack%20(CCM)#action=com.ibm.team.workitem.runSavedQuery&id=_GTAYo_FDEe-LqNoB04ZrZg", "MPCI_SW_SYS_OlderProblems_3Months_Diag"),
    ("OPMM Team", "https://rb-alm-14-p.de.bosch.com/ccm/web/projects/CentralComputingRack%20(CCM)#action=com.ibm.team.workitem.runSavedQuery&id=_ahnnAvFDEe-LqNoB04ZrZg", "MPCI_SW_SYS_OlderProblems_3Months_OPMM"),
    ("Safety Team", "https://rb-alm-14-p.de.bosch.com/ccm/web/projects/CentralComputingRack%20(CCM)#action=com.ibm.team.workitem.runSavedQuery&id=_hslY4vFDEe-LqNoB04ZrZg", "MPCI_SW_SYS_OlderProblems_3Months_Safety"),
    ("Security Team", "https://rb-alm-14-p.de.bosch.com/ccm/web/projects/CentralComputingRack%20(CCM)#action=com.ibm.team.workitem.runSavedQuery&id=_lzEtIvFDEe-LqNoB04ZrZg", "MPCI_SW_SYS_OlderProblems_3Months_Security"),
    ("MaaS Team", "https://rb-alm-14-p.de.bosch.com/ccm/web/projects/CentralComputingRack%20(CCM)#action=com.ibm.team.workitem.runSavedQuery&id=_rSRgyPFDEe-LqNoB04ZrZg", "MPCI_SW_SYS_OlderProblems_3Months_MaaS"),
    ("DRB Team", "https://rb-alm-14-p.de.bosch.com/ccm/web/projects/CentralComputingRack%20(CCM)#action=com.ibm.team.workitem.runSavedQuery&id=_xJUzsvFDEe-LqNoB04ZrZg", "MPCI_SW_SYS_OlderProblems_3Months_DRB"),
]

# Different symbols for teams
team_symbols = {
    "COM Team": "🖥️",
    "Diag Team": "🩺",
    "OPMM Team": "⚙️",
    "Safety Team": "🛡️",
    "Security Team": "🔒",
    "MaaS Team": "☁️",
    "DRB Team": "📚"
}

# Function to delete old CSV files
def delete_old_csvs(download_folder, keyword):
    for file in os.listdir(download_folder):
        if file.endswith(".csv") and keyword in file:
            os.remove(os.path.join(download_folder, file))
            print(f"Deleted old file: {file}")

# Set up WebDriver
driver = webdriver.Chrome()

# For collecting all team tables
full_html_body = ""

# Current date
today = datetime.today()

for team_title, rtc_url, filename_keyword in teams_info:
    delete_old_csvs(download_path, filename_keyword)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(rtc_url)

    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'jazz_ui_toolbar_Button_1')))
        download_button = driver.find_element(By.ID, 'jazz_ui_toolbar_Button_1')
        download_button.click()
    except Exception as e:
        print(f"Download button not found for {team_title}: {e}")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        continue

    time.sleep(10)

    def get_latest_csv(download_folder, keyword):
        files = [os.path.join(download_folder, f) for f in os.listdir(download_folder) if f.endswith(".csv") and keyword in f]
        return max(files, key=os.path.getctime) if files else None

    latest_csv = get_latest_csv(download_path, filename_keyword)

    if not latest_csv or os.path.getsize(latest_csv) <= 1024:
        print(f"No valid CSV downloaded for {team_title}")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        continue

    df = pd.read_csv(latest_csv, encoding="utf-16", delimiter="\t")

    for col in ["Id", "Summary", "Severity", "Creation Date", "Exclude"]:
        if col not in df.columns:
            df[col] = ""

    def convert_to_days(date_str):
        if pd.isna(date_str):
            return "Unknown"
        formats = [
            "%b %d, %Y, %I:%M %p", "%b %d, %Y %I:%M %p",
            "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S",
            "%d.%m.%Y %H:%M"
        ]
        for fmt in formats:
            try:
                return (today - datetime.strptime(date_str.strip(), fmt)).days
            except ValueError:
                continue
        print(f"Unrecognized date format: {date_str}")
        return "Unknown"

    df["Days Ago"] = df["Creation Date"].apply(convert_to_days)

    def color_days_ago(days, exclude):
        if str(exclude).strip().lower() == "yes":
            return f"<td>{days}</td>"
        if isinstance(days, int):
            if days > 100:
                return f'<td style="background-color: red; color: white; font-weight: bold;">{days}</td>'
            elif days > 90:
                return f'<td style="background-color: orange; color: black; font-weight: bold;">{days}</td>'
        return f"<td>{days}</td>"

    symbol = team_symbols.get(team_title, "🔵")

    html_table = f"""
    <h2 style="color: #2E86C1;">{symbol} {team_title}</h2>
    <p><a href="{rtc_url}" style="font-weight: bold; text-decoration: none; color: #117A65;">🔗 RTC Query Link</a></p>
    <table style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; font-size: 14px;">
        <tr style="background-color: gray; color: white;">
            <th style="border: 1px solid black; padding: 8px;">ID</th>
            <th style="border: 1px solid black; padding: 8px;">Summary</th>
            <th style="border: 1px solid black; padding: 8px;">Severity</th>
            <th style="border: 1px solid black; padding: 8px;">Days Ago</th>
        </tr>
    """

    for _, row in df.iterrows():
        id_val = row["Id"]
        summary = row["Summary"]
        severity = row["Severity"]
        exclude_flag = row["Exclude"]
        days_ago_html = color_days_ago(row["Days Ago"], exclude_flag)

        rtc_ticket_url = f"https://rb-alm-14-p.de.bosch.com/ccm/web/projects/CentralComputingRack%20(CCM)#action=com.ibm.team.workitem.viewWorkItem&id={id_val}"
        id_link = f'<td style="border: 1px solid black; padding: 8px;"><a href="{rtc_ticket_url}" target="_blank" style="color: blue; font-weight: bold;">{id_val}</a></td>'
        html_table += f"<tr>{id_link}<td style='border: 1px solid black; padding: 8px;'>{summary}</td><td style='border: 1px solid black; padding: 8px;'>{severity}</td>{days_ago_html}</tr>"

    html_table += "</table><br><br>"

    full_html_body += html_table

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

driver.quit()

# Outlook Email Setup
outlook = win32com.client.Dispatch("Outlook.Application")
mail = outlook.CreateItem(0)

#mail.To = "Guruprasad.Mangali@in.bosch.com"
#mail.CC = "Guruprasad.Mangali@in.bosch.com"


mail.To = "Shrihari.Jamadagni@in.bosch.com; NikhilS.Bharadwaj@in.bosch.com; spai.aiswarya@in.bosch.com; abdulbasit.salim@my.bosch.com; Kavya.Rajkumar@in.bosch.com; Sreelesh.Uv@in.bosch.com; tarunkumar.bansal@in.bosch.com; prajaktamadhukar.wadhone@in.bosch.com"
mail.CC = "Haasine.Chandrasekar@in.bosch.com; Manickam.Chokkalingam@in.bosch.com; NateshKumar.Kalasetty@in.bosch.com; Pavitra.NV@in.bosch.com; sathyan.krishnamoorthy@in.bosch.com; muhammadirfan.rafique@de.bosch.com; senthilrajan.arunachalam@in.bosch.com;Vrushali.Rao2@in.bosch.com; Hemeema.Kotla@in.bosch.com; Sushma.CR@in.bosch.com; PrajaktaMadhukar.Wadhone@in.bosch.com; Laxmi.Adagal@in.bosch.com;"


mail.Subject = f"[Automated] RTC Report: Problem Tickets Older Than 3 Months ({today_date})"

# Email Body
mail.HTMLBody = f"""
<p>Hello Everyone,</p>

<p>Please find attached the RTC report containing problem tickets that are older than 3 months. You can also check the latest status through the live RTC query mentioned in the link below.</p>

{full_html_body}

<p>Best regards,<br><b>MPCI Automation 🤖</b></p>
"""

mail.Send()

print("✅ Email sent successfully with details for all teams.")
