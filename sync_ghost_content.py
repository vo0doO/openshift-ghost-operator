import logging
import os
import sys
import time

from get_token import get_token
from run_cmd import run_command, run_commands

time = time.asctime().replace(" ", "-")
logger = logging.getLogger(__name__)

token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token")
pod_content_dir = "/var/lib/ghost/"
local_content_dir = "c:/Users/vo0/.ghost/"
local_backups_content_dir = "c:/Users/vo0/.ghost/backups/"
pod_name=str

system_command = {
    "login": f"oc login https://api.pro-eu-west-1.openshift.com --token={get_token(token_path=token_path, password='p')}",
    "get_pod": "oc get pods -l app=ghostis -o name",
    "sync": f"oc rsync {local_content_dir} {pod_name}:{pod_content_dir} --exclude=current --include=content.orig --no-perms",
    "local_backup": f"cp -r {local_content_dir} {local_backups_content_dir}[{time}]",
}


if __name__ == "__main__":
    try:
        run_command(system_command["login"])
        pod_name = run_command(system_command["get_pod"]).replace("pod/", "")
        logger.info(f" {pod_name}")
        # run_command(system_command["local_backup"])
        run_command(system_command["sync"])
        s = ""
    except Exception as e:
        logger.error(f"{e}")
