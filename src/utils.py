#!.\.venv\Scripts\ python
# -*- coding: utf-8 -*-

import os
import sys
import cmdl
import time
import shutil
import base64
import hashlib
import logging
from site import venv
from functools import reduce
from get_token import get_token
from argparse import ArgumentError

APP_NAME = "ghostis"
BLOG_URL = "https://blog.vo.dedyn.io"
FILENAME_FOR_CREATE = str
GHOST_CONTENT_ITEMS_DIRS = ["images", "themes",
                            "logs", "settings", "data", "public"]
GHOST_ROOT_DIRS = ["content.orig", "content", ".vs-code"]
GHOST_ROOT_FILES = [".ghost-cli", "config.production.json"]
LOCAL_GHOST_BACKUP_PATH = "c:\\home\\vo0\\ghost\\backups"
LOCAL_GHOST_CONTENT_PATH = "/home/vo0/ghost/current/content"
LOCAL_GHOST_GOGLE_DRIVE_PATH = "c:\\home\\vo0\\ghost\\gdrive"
LOCAL_GHOST_PATH = "/home/vo0/ghost/current"
LOCAL_GHOST_PATH_FOR_BACKUP = "c:\\home\\vo0\\ghost\\current"
LOGS_FILE_NAME = "logs.log"
POD_GHOST_CONTENT_PATH = "/var/lib/ghost/content"
POD_GHOST_PATH = "/var/lib/ghost"
POD_NAME = cmdl.run(f"oc get pods -l app={APP_NAME} -o name").replace("pod/", "")
PROJECT_NAME = "sso"
TOKEN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token")
COMMANDS = {
    "backup_current_local_files": 'shutil.copytree(f"{LOCAL_GHOST_PATH_FOR_BACKUP}", f"{LOCAL_GHOST_BACKUP_PATH}\\ghost[{my_time}]", symlinks=False, ignore=None, copy_function=shutil.copy2, ignore_dangling_symlinks=False, dirs_exist_ok=False)',
    "login_to_cluster": f"oc login https://api.pro-eu-west-1.openshift.com --token={get_token(token_path=TOKEN_PATH, password='p')}",
    "set_project": f"oc project {PROJECT_NAME}",
    "get_pod_name": f"oc get pods -l app={APP_NAME} -o name",
    "copy_all_ghost_content_dirs_from_local_to_pod": f"oc cp {LOCAL_GHOST_CONTENT_PATH} {PROJECT_NAME}/{POD_NAME}:{POD_GHOST_PATH}",
    "copy_once_ghost_content_dir_from_local_to_pod": f"oc cp {LOCAL_GHOST_CONTENT_PATH}/{GHOST_CONTENT_ITEMS_DIRS[0]} {PROJECT_NAME}/{POD_NAME}:{POD_GHOST_CONTENT_PATH}",
    "copy_all_ghost_dirs_from_pod_to_local": f"oc cp {PROJECT_NAME}/{POD_NAME}:{POD_GHOST_PATH} {LOCAL_GHOST_PATH}",
    "copy_all_ghost_content_dirs_from_pod_to_local": f"oc cp {PROJECT_NAME}/{POD_NAME}:{POD_GHOST_CONTENT_PATH} {LOCAL_GHOST_PATH}",
    "copy_once_ghost_content_dir_from_local_to_pod": f"oc cp {PROJECT_NAME}/{POD_NAME}:{POD_GHOST_CONTENT_PATH}/{GHOST_CONTENT_ITEMS_DIRS[0]} {LOCAL_GHOST_CONTENT_PATH}/{GHOST_CONTENT_ITEMS_DIRS[0]} ",
    "create_empty_dir_in_pod": f"oc exec {POD_NAME} mkdir content/{GHOST_CONTENT_ITEMS_DIRS[0]}",
    "create_empty_file_in_pod": f"oc exec {POD_NAME} touch content/{FILENAME_FOR_CREATE}",
    "get_folders_in_pod": f"oc exec {POD_NAME} -- ls content/",
    "run_ghost": f"oc exec {POD_NAME} -- node current/index.js --url={BLOG_URL}",
}


logger = logging.getLogger("Sync my ghost openshift")


def get_time() -> str:
    try:
        return time.asctime().replace(" ", "_").replace(":", "-")
    except Exception as e:
        logger.info("Error on clean logs", e.with_traceback)


def hash_files(files, verbose=False):
    """
    Хэши содержание данных файлов с использованием алгоритма MD5 в отсортированном порядке
    """

    m = hashlib.md5()
    for file in sorted(files):
        if verbose:
            file_hasher = hashlib.md5()
        with open(file, "rb") as f:
            content = f.read()
            m.update(content)
            if verbose:
                file_hasher.update(content)
        if verbose:
            print(file_hasher.hexdigest(), file=file)
    return m.hexdigest()


def set_logger():
    logging.basicConfig(
        filename="logs.log",
        filemode="a",
        format="%(asctime)s:%(levelname)s:%(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger("Sync my ghost openshift")
    return logger


def clear_logs(file_name) -> None:
    if file_name is None:
        raise ArgumentError("Not specified Log file name")
    try:
        with open(file_name, "r") as logs:
            lines = logs.readlines()
            lines_len = len(lines)
        if lines_len < 300:
            logger.info("Logs do not need cleaning")
            return
        with open("logs.log", "w") as logs:
            for line in lines[len(lines) - 200: -1]:
                logs.write(line)
        logger.info("Clean logs success")
    except Exception as e:
        logger.info(f"Error on clean logs: {e.with_traceback}")


def clear_backups(folder: str) -> None:
    if folder is None:
        raise ArgumentError("Backups folder is not specified.")
    try:
        backups_dirs = sorted(os.listdir(folder))
        if len(backups_dirs) < 5:
            logger.info("Backups do not need cleaning")
            return

        for dir in backups_dirs[0: len(backups_dirs) - 3]:
            shutil.rmtree(f"{folder}\\{dir}", ignore_errors=True)
        logger.info("Clean local backup success")
    except Exception as e:
        logger.info(f"Error on clean logs, {e.with_traceback}")


def backup_local_files() -> None:
    try:
        shutil.copytree(
            f"{LOCAL_GHOST_PATH_FOR_BACKUP}",
            f"{LOCAL_GHOST_BACKUP_PATH}\\ghost[{get_time()}]",
            symlinks=False,
            ignore=None,
            copy_function=shutil.copy2,
            ignore_dangling_symlinks=False,
            dirs_exist_ok=False,
        )
        logger.info("Local files {} backup success")
    except Exception as e:
        logger.info(f"Error on clean logs, {e.with_traceback}")


def clear_local_archives_folder(folder) -> None:
    try:
        files = sorted(os.listdir(folder))
        if len(files) < 5:
            logger.info(
                "Local archives for google drive don't need more cleaning")
        elif len(files) > 5:
            for file in files[0:len(files) - 3]:
                if ".zip" in file:
                    os.remove(f"{folder}\\{file}")
    except Exception as e:
        logger.info(f"Error on make archive, {e.with_traceback}")


def make_archive_for_google_drive(folder):
    try:
        for dir in sorted(os.listdir(LOCAL_GHOST_BACKUP_PATH)):
            shutil.make_archive(
                f"{folder}\\{dir}", "zip", f"{LOCAL_GHOST_BACKUP_PATH}\\{dir}"
            )
    except Exception as e:
        logger.info(f"Error on make archive, {e.with_traceback}")


def sanitize_folders_in_pod_str(folders_in_pod) -> str:
    if not folders_in_pod:
        logging.raiseExceptions("Not 'folder_in_pods'")
    s = reduce(lambda folders, x: f'{folders} | {x}', reduce(lambda chars, x: f'{chars}{x}', list(map(
        lambda char: ' ' if b'Cg==' in base64.standard_b64encode(char.encode('utf-8')) else char, list(folders_in_pod)))).split(' '))
    return s


def download_current_content_from_pod_to_local(pod_name: str, project_name: str, src_path: str, dst_path: str, folders_list: list[str], files_list: list[str]) -> None:
    for dir in folders_list:
        try:
            cmdl.run(f"oc cp {project_name}/{pod_name}:{src_path}/{dir}/ {dst_path}/{dir}")
            time.sleep(3)
            logger.info(f"Copy {dir} from pod to local success")
        except Exception as e:
            logger.info(f"Error on download files from pod: {e.args}")
            continue
    for file in files_list:
        try:
            cmdl.run(f"oc cp {project_name}/{pod_name}:{src_path}/{file} {dst_path}/{file}")
            time.sleep(3)
            logger.info(f"Copy {file} from pod to local success")
        except Exception as e:
            logger.info(f"Error on download files from pod: {e.args}")
            continue