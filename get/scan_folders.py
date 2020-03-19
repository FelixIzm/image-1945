from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from string import Template
import pprint
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'obd.json'
credentials = service_account.Credentials.from_service_account_file(os.path.join(BASE_DIR, SERVICE_ACCOUNT_FILE), scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)
name_root_folder = 'Folder'
#root_results = service.files().list(pageSize=10,fields="nextPageToken, files(id, name, mimeType,webViewLink)",q=Template("name contains '$name_root_folder'").safe_substitute(name_root_folder=name_root_folder)).execute()
#id_root_folder = root_results['files'][0]['id']
d = datetime.utcnow() - timedelta(days=4)
#time_obj=datetime.strptime(d,'%Y-%m-%dT%H:%M:%S')
#print(time_obj)
print(d)

pp = pprint.PrettyPrinter(indent=4)
#var ThirtyDaysBeforeNow = new Date().getTime()-3600*1000*24*30;

#results = service.files().list(pageSize=1000, fields="nextPageToken, files(createdTime, name)",q = "mimeType='application/vnd.google-apps.folder' and not 'root' in parents and trashed=false and createdTime < '{}'".format(d.strftime('%Y-%m-%d'))).execute()
results = service.files().list(pageSize=1000, fields="nextPageToken, files(createdTime, name, id)",q = "not 'root' in parents and trashed=false and createdTime < '{}'".format(d.strftime('%Y-%m-%d'))).execute()
items = results.get('files', [])
#pp.pprint(items)
#print(len(items))
for item in items:
    try:
        service.files().delete(fileId=item['id']).execute()
        print(item['id'])
    except HttpError as e:
        print('Asssn error occurred: %s' % e)

