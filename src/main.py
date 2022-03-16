#!.\.venv\Scripts\ python
# -*- coding: cp1252 -*-


import sys
import logging
from utils import *
from gdrive import *
from cmdl import run


def main():
    try:
        clear_logs(LOGS_FILE_NAME)
        run(COMMANDS["login_to_cluster"])
        logger.info("Login to cluster success")
        run(COMMANDS["set_project"])
        logger.info(f"Set project with name: {PROJECT_NAME}")
        POD_NAME = run(COMMANDS["get_pod_name"]).replace("pod/", "")
        logger.info(f"Set pod with name: {POD_NAME}")
        folders_in_pod = run(f"oc exec {POD_NAME} -- ls content/")
        logger.info(f"Pod have {sanitize_folders_in_pod_str(folders_in_pod)} in content")
        if folders_in_pod != "":
            logger.info(
                "Pod is not new - we do only backup in it, do not copy anything")
            clear_backups(LOCAL_GHOST_BACKUP_PATH)
            backup_local_files()
            download_current_content_from_pod_to_local(
                POD_NAME, PROJECT_NAME, POD_GHOST_PATH, LOCAL_GHOST_PATH, GHOST_ROOT_DIRS, GHOST_ROOT_FILES
                )
            clear_local_archives_folder(LOCAL_GHOST_GOGLE_DRIVE_PATH)
            logger.info("Clean in archive folder success")
            make_archive_for_google_drive(
                LOCAL_GHOST_GOGLE_DRIVE_PATH)
            logger.info("Created archive from current ghost files success")
            logger.info("Uploading backups in cloud")
            drive = get_service()
            clear_files_in_google_drive(drive)
            upload_file_in_google_drive(LOCAL_GHOST_GOGLE_DRIVE_PATH, drive)
            logger.info("Cleaning ghost archive files in google drive")
            logger.info("[+]"*20)
            return
        if folders_in_pod == "":
            logger.info("Pod is new - just copy to it, not making backup")
            run(COMMANDS["copy_all_ghost_content_dirs_from_local_to_pod"])
            logger.info("Copy content files from local to pod success")
            run(COMMANDS["run_ghost"])
            logger.info("Start ghost server success")
            logger.info("Program finished this work")
            return
    except Exception as e:
        logger.error(f"Error in main: {e.args}")
if __name__ == "__main__":
    logger = set_logger()
    logger.info("[+]"*20)
    main()
