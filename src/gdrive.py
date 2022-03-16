from __future__ import print_function
import logging

import os
from os import error as e
from functools import reduce

from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import client, file, tools

from utils import LOCAL_GHOST_GOGLE_DRIVE_PATH

l = logging.getLogger("Sync my ghost openshift")
SCOPES = ['https://www.googleapis.com/auth/drive']

def logs(f):
    """
    Decorator
    for logging calling 
    functions and arguments

    :param f: functon for logging
    """

    if not f:
        raise e(e)

    def wraps(*args):
        try:
            if not args:
                return
            print(f"Calling function '{f.__name__}'")
            return f(args)
        except Exception as e:
            l.info(f"Error in :param logs: {e}")
    return wraps


def get_service():
    store = file.Storage('src/storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('src/client_id.json', SCOPES)
        creds = tools.run_flow(flow, store)
    HTTP = creds.authorize(Http())
    DRIVE = discovery.build('drive', 'v3', http=HTTP)
    SHEETS = discovery.build('sheets', 'v4', http=HTTP)
    l.info("Connect to google service success")
    return DRIVE


def clear_files_in_google_drive(DRIVE):
    """Deleted must more
    files on what you want

    :param DRIVE: request объект запроса
    к конечной точке api google drive 
    """

    if not DRIVE:
        return
    try:
        gdrive_backups_folder_id = "1iRH-NKzG3eUFQ1qXwVo2wt4ynEobRlCP"
        files = ls(gdrive_backups_folder_id, DRIVE)
        file_ids = files["ids"]
        try:
            if len(file_ids) < 5:
                l.info("Google drive do not need clean")
                return
            for id in file_ids[0:len(file_ids)-3]:
                l.info(
                    f"Deleted deprecated file in google drive: {DRIVE.files().get(fileId=id).execute().get('name')}")
                DRIVE.files().delete(fileId=id).execute()
            return
        except Exception as e:
            l.info(f"Error on clean gdrive files: {e.args}")
    except Exception as e:
        l.info("Error in clean_files_in_google_drive: {e}")


def upload_file_in_google_drive(src_folder, DRIVE):
    """
    Upload all files from
    local backup directory
    to pod content directory

    :param src_folder: this path to local backups
    """

    if not src_folder:
        e = e('Not src folder name')
        l.info(e)
        raise e
    try:
        gdrive_folder_id = "1iRH-NKzG3eUFQ1qXwVo2wt4ynEobRlCP"
        files_in_src = set(os.listdir(src_folder))
        files_in_dst = set(ls(gdrive_folder_id, DRIVE)["names"])
        files_diff = files_in_src.difference(files_in_dst)
        if len(files_diff) < 1:
            l.info("All archives upload in google drive before this time")
            return
        l.info(
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
                l.info(
                    f"File Name : {filename} upload in google drive")
            except Exception as e:
                l.info(f"Error on upload files to gdrive: {e.with_traceback}")
    except Exception as e:
        l.info(f"Error on upload files to gdrive: {e.with_traceback}")


def ls(folder_id: str, DRIVE) -> list[str]:
    """
    Возвращает отсортированный по имени
    массив с именами файлов зарегистрированных
    в директории

    :param folder_id: id директории
    :param DRIVE: request объект запроса
    к конечной точке api google drive
    """

    file_names = list()
    file_ids = list()

    try:

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
        l.info(f"Error on clean gdrive files: {e.args}")


#####################
## Only for debbug ##
#####################
# DRIVE = get_service()
# upload_file_in_google_drive(LOCAL_GHOST_GOGLE_DRIVE_PATH, DRIVE)
# clear_files_in_google_drive(DRIVE)
