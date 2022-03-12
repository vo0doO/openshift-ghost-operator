import logging

from gdrive import *
from cmdl import run
from utils import *


def main():

    logging.basicConfig(
        filename="logs.log",
        filemode="a",
        format="%(asctime)s:%(levelname)s:%(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger("Sync my ghost openshift")

    try:

        logger.info("Start program")

        
        clear_logs(LOGS_FILE_NAME)
        logger.info("Clean logs success")

        
        run(COMMANDS["login_to_cluster"])
        logger.info("Login to cluster success")

        run(COMMANDS["set_project"])
        logger.info(f"Set project with name: {PROJECT_NAME}\n")

        POD_NAME = run(COMMANDS["get_pod_name"]).replace("pod/", "")
        logger.info(f"Set pod with name: {POD_NAME}\n")

        folders_in_pod = run(f"oc exec {POD_NAME} -- ls content/")
        logger.info(f"Pod have this content folders: {folders_in_pod.replace('\n', ' ')}")

        if folders_in_pod != "":
            logger.info("Pod is not new - we do only backup in it do not copy anything")

            clear_backups(LOCAL_GHOST_BACKUP_PATH)
            logger.info("Clean local backup success")

            backup_local_files()
            logger.info("Local files backup success\n")

            run(COMMANDS["copy_all_ghost_dirs_from_pod_to_local"])
            logger.info("Copy files from pod success\n")

            archive_name = f"ghost[{get_time()}]"

            make_archive_for_google_drive(LOCAL_GHOST_GOGLE_DRIVE_PATH, archive_name)
            logger.info("Created archive from current ghost files\n")

            upload_file_in_google_drive(LOCAL_GHOST_GOGLE_DRIVE_PATH, archive_name)
            logger.info("Uploading archive from current ghost files to google drive\n")

            clear_files_in_google_drive()
            logger.info("Cleaned ghost archive files in google drive\n")

            logger.info("Program finished this work")
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
    main()
