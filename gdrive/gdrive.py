from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import datetime
from natsort import natsorted
from tqdm import tqdm

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
this_file_path = os.path.abspath(os.path.dirname(__file__))
date_now = datetime.date.today()#今日の日付

def init():
    # """
    # Shows basic usage of the Drive v3 API.
    # Prints the names and ids of the first 10 files the user has access to.
    # """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(this_file_path + '/token.pickle'):
        with open((this_file_path + '/token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(this_file_path + '/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    return service

def get_latest_file():
    service = init()

    listRequest = service.files().list(q="'16mxDL5lyZsVYDuiJqNVT3o-RI5TuMX5m' in parents and mimeType = 'video/quicktime'")

    target_dir = listRequest.execute().get('files')

    target_file = target_dir[0]

    print("new file check")
    last_id = None
    with open(this_file_path + "/last_id.txt", 'r') as file:
        last_id = file.read()

    if last_id == target_file.get('id'):
        return False
    else:
        with open(this_file_path + "/last_id.txt", 'w') as file:
            file.write(target_file.get('id'))
        
    # download target file
    print("download MOV file from google drive")
    with open(this_file_path + '/../img/target.MOV', 'wb') as file:
        request = service.files().get_media(fileId=target_file.get('id'))
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        print("Download %d%%." % int(status.progress() * 100))
    
    return True

def upload_imgs(imgs_dir):
    service = init()
    file_metadata = {
        'name': str(date_now),
        # TNSKSpoiler/slides/
        'parents': ['1ZHXnYrBY-iY6RMHbhfCmVbO9YRucqQYD'],
        'mimeType': 'application/vnd.google-apps.folder'
    }

    print("confirming google drive folder")

    # すでにディレクトリが存在していれば、そこに保存
    listRequest = service.files().list(q="name = '{0}' and '1ZHXnYrBY-iY6RMHbhfCmVbO9YRucqQYD' in parents and trashed = false".format(date_now))
    target_dir = listRequest.execute().get('files')

    # フォルダの取得 || 作成
    target_dir_id = None
    if target_dir:
        target_dir_id = target_dir[0].get('id')
    else:
        upload_dir = service.files().create(body=file_metadata,
                                            fields='id').execute()
        print('Folder ID: %s' % upload_dir.get('id'))
        target_dir_id = upload_dir.get('id')


    files = natsorted(os.listdir(imgs_dir))

    print("uploading slides")
    for name in tqdm(files):
        file_metadata = {'name': name, 
                        'parents': ['{0}'.format(target_dir_id)],
                        'mimetype': 'image/png'  }
        media = MediaFileUpload(imgs_dir + name,
                        mimetype='image/png')
        file = service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        # print('Upload File\nFile ID: %s' % file.get('id'))

    print("slides are uploaded to google drive: slide/" + str(date_now) + "/")


# def main():
#     service = init()
    

# if __name__ == '__main__':
#     main()