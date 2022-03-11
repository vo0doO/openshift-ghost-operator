import logging
from cmd import run

from vars import *

logger = logging.getLogger(__name__)


try:
    run(COMMANDS["login"])
    POD_NAME = run(COMMANDS["get_pod"]).replace("pod/", "")
    logger.info(f"Set project {PROJECT_NAME}, work with pod: {POD_NAME}")
    # run(SYSTEM_COMMAND["local_backup"])
    run(COMMANDS["sync"])
    s = ""
except Exception as e:
    logger.error(f"{e}")
