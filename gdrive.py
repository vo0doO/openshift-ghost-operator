from __future__ import print_function

import logging
from msilib.schema import Error

from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import client, file, tools

logger = logging.getLogger("Sync my ghost openshift")

# Если модифицируете эти обзоры, удалите файл token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_service():
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
        creds = tools.run_flow(flow, store)
    HTTP = creds.authorize(Http())
    DRIVE = discovery.build('drive', 'v3', http=HTTP)
    SHEETS = discovery.build('sheets', 'v4', http=HTTP)
    logger.info("Connect to google service success")
    return DRIVE, SHEETS

def upload_file_in_google_drive(folder, filename):
    if folder is None or filename is None:
        raise Error("Folder or fie name is none")
    try: 
        DRIVE, SHEETS = get_service()
        gdrive_folder_id = "1iRH-NKzG3eUFQ1qXwVo2wt4ynEobRlCP"
        file_metadata = {
            'name': f"{filename}.zip",
            'mimeType': 'application/x-zip-compressed',
            'parents': [gdrive_folder_id]
        }

        media = MediaFileUpload(
            f"{folder}\\{filename}.zip",
            mimetype='application/x-zip-compressed',
            resumable=True)

        file = DRIVE.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

        logger.info(f"File Name : {file.get('name')} upload in google drive")
    except Exception as e:
        logger.error("Error on upload files to gdrive", e.with_traceback)

def clear_files_in_google_drive():
    backups_files = list()
    try:
        DRIVE, SHEETS = get_service()
        gdrive_backups_folder_id = "1iRH-NKzG3eUFQ1qXwVo2wt4ynEobRlCP"

        response = DRIVE.files().list(
            q="mimeType='application/x-zip-compressed'",
            spaces='drive',
            fields='files(id, name, parents)'
            ).execute()
        files = response.get('files', [])
        
        count = 0
        for file in files:
            count += 1
            if not 'parents' in file:
                continue
            if not gdrive_backups_folder_id in file['parents'][0]:
                continue
            if file['name'] == files[count]['name']:
                logger.info(f"Deleted dublicate file in google drive, File Name: {file.get('name')}")
                DRIVE.files().delete(fileId=file.get('id')).execute()
                continue
            f = DRIVE.files().get(fileId=file.get('id')).execute()
            backups_files.append(f)
        
        if len(backups_files) < 4:
            logger.info("Google drive backups don't need more cleaning")
            return

        for file in backups_files[0:len(backups_files)-3]:
            logger.info(f"Deleted deprecated file in google drive: {file.get('name')}")
            DRIVE.files().delete(fileId=file.get('id')).execute()


    except Exception as e:
        logger.error("Error on clean gdrive files", e.args)