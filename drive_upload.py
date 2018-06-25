from pydrive import auth
from pydrive.drive import GoogleDrive
import os, sys


def authenticate():
    gauth = auth.GoogleAuth(settings_file="settings.yaml")
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("credentials.json")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("credentials.json")

    print("Google Drive authentication complete")

    # create a drive object
    drive = GoogleDrive(gauth)
    return drive


def upload_results(appname, drive):
    folder = appname
    folder_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    for fol in folder_list:
        if fol['title'] == folder:
            # if the folder is already created then delete it and create a new one
            fol.Trash()
            break

    created_folder = drive.CreateFile({'title': folder, "mimeType": "application/vnd.google-apps.folder"})
    created_folder.Upload()
    permission = created_folder.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'writer'})

    download_link = created_folder['alternateLink']

    parent_id = created_folder["id"]

    print("Folder check complete")

    for file in (os.listdir("analysis/plots")):
        folder_path = os.path.join(os.getcwd(), "analysis/plots/")
        # if this doest work chdir here and then change back before return
        drive_container = drive.CreateFile({"title": file, "parents": [{"kind": "drive#fileLink", "id": parent_id}]})
        drive_container.SetContentFile(folder_path + file)
        drive_container.Upload()
        print(file+" uploaded")

    return download_link

