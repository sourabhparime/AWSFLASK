from pydrive import auth
from pydrive.drive import GoogleDrive
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
