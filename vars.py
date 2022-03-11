import os
import time
from get_token import get_token

time = time.asctime().replace(" ", "-")


TOKEN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token")
POD_CONTENT_PATH = "/var/lib/ghost/"
LOCAL_CONTENT_DIR = "c:/Users/vo0/.ghost/"
LOCAL_BACKUP_CONTENT_DIR = "c:/Users/vo0/.ghost/backups/"
PROJECT_NAME = "sso"
APP_NAME = "ghostis"
POD_NAME=str

SYSTEM_COMMAND = {
    "login": f"oc login https://api.pro-eu-west-1.openshift.com --token={get_token(token_path=TOKEN_PATH, password='p')}",
    "set_project": f"oc project {PROJECT_NAME}",
    "get_pod": f"oc get pods -l app={APP_NAME} -o name",
    "cp_from_pod": f"oc cp {LOCAL_CONTENT_DIR} {POD_NAME}:{POD_CONTENT_PATH}",
    "local_backup": f"cp -r {LOCAL_CONTENT_DIR} {LOCAL_BACKUP_CONTENT_DIR}[{time}]",
}
