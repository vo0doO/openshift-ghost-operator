
import logging

from cmdl import run
from utils import *


def main():
    logging.basicConfig(filename='logs.log', filemode='a', format=f'{get_time()}:%(levelname)s:%(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    try:
        logger.info("Start program")

        logger.info("Start clear logs")
        clear_logs(LOGS_FILE_NAME)
        logger.info("Finish clear logs\n")

        logger.info("Start login to cluster")
        run(COMMANDS["login_to_cluster"])
        logger.info("Finish login to cluster\n")

        logger.info("Start set project")
        run(COMMANDS["set_project"])
        logger.info(f"Work with project: {PROJECT_NAME}")
        logger.info("Finish set project\n")

        logger.info("Start set pod name")
        POD_NAME = run(COMMANDS["get_pod_name"]).replace("pod/", "")
        logger.info(f"Work with pod: {POD_NAME}")
        logger.info("Finish set pod name\n")
        
        folders_in_pod = run(f"oc exec {POD_NAME} -- ls content/")
        
        
        if folders_in_pod != '':
            logger.info("Copy not new - we do only backup in it do not copy anything")

            logger.info("Start clear backup")
            clear_backups(LOCAL_GHOST_BACKUP_PATH)
            logger.info("Finish clear backup\n")

            logger.info("Start local backup")
            backup_local_files()
            logger.info("Finish local backup\n")

            run(COMMANDS["copy_all_ghost_dirs_from_pod_to_local"])
            return
        if folders_in_pod == '':
            logger.info("Copy new - just copy to it, not making backup")
            run(COMMANDS["copy_all_ghost_content_dirs_from_local_to_pod"])
            logger.info("Run ghost start")
            run(COMMANDS["run_ghost"])
            logger.info("Run ghost complete")
            return
    except Exception as e:
        logger.error(f"{e}")


if __name__ == "__main__":
    main()
