import time, json
import smtplib
from email.message import EmailMessage
import props

import drive_upload
global_flags = {"appname": "", "mail": "", "download_link": "", "begin_upload": "FALSE"}

with open("globals.json", "w") as fp:
    json.dump(global_flags, fp)


def upload_results():
    with open('globals.json', 'r') as fp:
        active_flags = json.load(fp)
    if active_flags["begin_upload"] == "TRUE":
        print("received app " + active_flags["appname"] + " for upload")
        drive = drive_upload.authenticate()
        download_link = drive_upload.upload_results(active_flags["appname"], drive)
        global_flags["download_link"] = download_link
        global_flags["send_mail"] = "TRUE"
        with open("globals.json", "w") as fp:
            json.dump(global_flags, fp)

        msg = EmailMessage()
        msg.set_content("Analysis request submitted by    " + active_flags["mail"] + " complete. Please visit " + download_link + " for results")
        msg['Subject'] = "Analysis Complete"
        msg['From'] = props.MAIL_USERNAME
        msg['To'] = active_flags["mail"]
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(props.MAIL_USERNAME, props.MAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        active_flags["begin_upload"] = "FALSE"
        active_flags["mail"] = ""
        active_flags["appname"] = ""
        with open("globals.json", "w") as fp:
            json.dump(global_flags, fp)
        return "Email Trigger set"

    return "Waiting for trigger"


i = 0
while True:
    i = i + 1
    print("wait cycle " + str(i))
    time.sleep(120)
    print(upload_results())
