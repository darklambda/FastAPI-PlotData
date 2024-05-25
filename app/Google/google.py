import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http

SCOPES = ["https://www.googleapis.com/auth/drive"]
KEY_FILE_LOCATION = './app/Google/credentials-sa.json'
FILE_ID = '1mh4ro8fPRdH3Rxn4fXEBvLYnWDUk4RoD'

def download_file():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)
    file = None
    try:
        # Call the Drive v3 API
        http_auth = credentials.authorize(Http())
        drive = build('drive', 'v3', http=http_auth)

        request = drive.files().get_media(fileId=FILE_ID)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        with open("./app/job-app-tmp.xlsx", "wb") as f:
            f.write(file.getbuffer())

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None
        

    