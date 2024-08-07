import io
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)


SCOPES = ["https://www.googleapis.com/auth/drive"]
KEY_FILE_LOCATION = './app/Google/credentials-sa.json'
FILE_ID = os.environ.get('FILE_ID')

def download_file(filename="job-app-tmp.xlsx"):
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
        while not done:
            _, done = downloader.next_chunk()
        with open("./app/" + filename, "wb") as f:
            f.write(file.getbuffer())

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None
        

    