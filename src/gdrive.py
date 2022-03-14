from __future__ import print_function
from functools import reduce

import logging
import os
from msilib.schema import Error

from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import client, file, tools

from utils import LOCAL_GHOST_GOGLE_DRIVE_PATH

logging.basicConfig(
    filename="logs.log",
    filemode="a",
    format="%(asctime)s:%(levelname)s:%(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("Sync my ghost openshift")

# Если модифицируете эти обзоры, удалите файл token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def get_service():
    store = file.Storage('src/storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('src/client_id.json', SCOPES)
        creds = tools.run_flow(flow, store)
    HTTP = creds.authorize(Http())
    DRIVE = discovery.build('drive', 'v3', http=HTTP)
    SHEETS = discovery.build('sheets', 'v4', http=HTTP)
    logger.info("Connect to google service success")
    return DRIVE


def upload_file_in_google_drive(src_folder, DRIVE):
    if not src_folder:
        raise AttributeError('Not src folder name')

    gdrive_folder_id = "1iRH-NKzG3eUFQ1qXwVo2wt4ynEobRlCP"
    files_in_src = set(os.listdir(src_folder))
    files_in_dst = set(ls(gdrive_folder_id, DRIVE)["names"])
    files_diff = files_in_src.difference(files_in_dst)
    if len(files_diff) < 1:
        logger.info("All archives upload in google drive before this time")
        return
    logger.info(
        f"Src folder have {reduce(lambda acc, s: f'{acc} | {s}', files_diff)} files to upload in google drive")
    for filename in files_diff:
        try:

            file_metadata = {
                'name': f"{filename}",
                'mimeType': 'application/x-zip-compressed',
                'parents': [gdrive_folder_id]
            }

            media = MediaFileUpload(
                f"{src_folder}\\{filename}",
                mimetype='application/x-zip-compressed',
                resumable=True)

            file = DRIVE.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

            logger.info(
                f"File Name : {filename} upload in google drive")
        except Exception as e:
            logger.error("Error on upload files to gdrive", e.with_traceback)


def clear_files_in_google_drive(DRIVE):
    gdrive_backups_folder_id = "1iRH-NKzG3eUFQ1qXwVo2wt4ynEobRlCP"
    files = ls(gdrive_backups_folder_id, DRIVE)
    file_ids = files["ids"]

    try:
        if len(file_ids) < 5:
            logger.info("Google drive do not need clean")
            return
        for id in file_ids[0:len(file_ids)-3]:
            logger.info(
                f"Deleted deprecated file in google drive: {DRIVE.files().get(fileId=id).execute().get('name')}")
            DRIVE.files().delete(fileId=id).execute()
        return

    except Exception as e:
        logger.error("Error on clean gdrive files", e.args)


def ls(folder_id: str, DRIVE) -> list[str]:
    file_names = list()
    file_ids = list()

    try:

        # folder_id = "1iRH-NKzG3eUFQ1qXwVo2wt4ynEobRlCP"

        response = DRIVE.files().list(
            q="mimeType='application/x-zip-compressed'",
            spaces='drive',
            fields='files(name, id, parents)',
            orderBy='name'
        ).execute()
        files = response.get('files', [])

        for file in files:
            if not 'parents' in file:
                continue
            if not folder_id in file['parents'][0]:
                continue
            f = DRIVE.files().get(fileId=file.get('id')).execute()
            file_names.append(f.get('name'))
            file_ids.append(f.get('id'))

        return {"names": file_names, "ids": file_ids}

    except Exception as e:
        logger.error("Error on clean gdrive files", e.args)
