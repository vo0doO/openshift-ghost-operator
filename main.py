import logging
from run_cmd import run_command


logger = logging.getLogger(__name__)


try:
    run_command(SYSTEM_COMMAND["login"])
    POD_NAME = run_command(SYSTEM_COMMAND["get_pod"]).replace("pod/", "")
    logger.info(f"Set project {PROJECT_NAME}, work with pod: {POD_NAME}")
    # run_command(SYSTEM_COMMAND["local_backup"])
    run_command(SYSTEM_COMMAND["sync"])
    s = ""
except Exception as e:
    logger.error(f"{e}")