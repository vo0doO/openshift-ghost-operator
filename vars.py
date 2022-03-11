import os
import time
from get_token import get_token

time = time.asctime().replace(" ", "-")

PROJECT_NAME = "ghost-test"
APP_NAME = "ghostis"
POD_NAME=str
BLOG_URL="https://blog.vo.dedyn.io"

TOKEN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token")
POD_GHOST_CONTENT_PATH = "/var/lib/ghost/content"
POD_GHOST_PATH = "/var/lib/ghost"
LOCAL_GHOST_PATH = "/home/vo0/ghost/current"
LOCAL_GHOST_CONTENT_PATH = "/home/vo0/ghost/current/content"
LOCAL_GHOST_BACKUP_PATH = "/home/vo0/ghost/backups"
GHOST_CONTENT_ITEMS_DIRS = [ "images", "themes", "logs", "settings", "data", "public"]
FILENAME_FOR_CREATE = str


SYSTEM_COMMAND = {
    "backup_current_local_files": f"cp -r {LOCAL_GHOST_PATH} {LOCAL_GHOST_BACKUP_PATH}[{time}]",


    "login_to_cluster": f"oc login https://api.pro-eu-west-1.openshift.com --token={get_token(token_path=TOKEN_PATH, password='p')}",
    "set_project": f"oc project {PROJECT_NAME}",
    "get_pod_name": f"oc get pods -l app={APP_NAME} -o name",


    "copy_all_ghost_content_dirs_from_local_to_pod": f"oc cp {LOCAL_GHOST_CONTENT_PATH} {PROJECT_NAME}/{POD_NAME}:{POD_GHOST_PATH}",
    "copy_once_ghost_content_dir_from_local_to_pod": f"oc cp {LOCAL_GHOST_CONTENT_PATH}/{GHOST_CONTENT_ITEMS_DIRS[0]} {PROJECT_NAME}/{POD_NAME}:{POD_GHOST_CONTENT_PATH}",


    "copy_all_ghost_dirs_from_pod_to_local": f"oc cp {POD_NAME}:{POD_GHOST_PATH} {LOCAL_GHOST_PATH}",
    "copy_all_ghost_content_dirs_from_pod_to_local": f"oc cp {PROJECT_NAME}/{POD_NAME}:{POD_GHOST_CONTENT_PATH} {LOCAL_GHOST_PATH}",
    "copy_once_ghost_content_dir_from_local_to_pod": f"oc cp {PROJECT_NAME}/{POD_NAME}:{POD_GHOST_CONTENT_PATH}/{GHOST_CONTENT_ITEMS_DIRS[0]} {LOCAL_GHOST_CONTENT_PATH}/{GHOST_CONTENT_ITEMS_DIRS[0]} ",


    "create_empty_dir_in_pod" : f"oc exec {POD_NAME} mkdir content/{GHOST_CONTENT_ITEMS_DIRS[0]}",
    "create_empty_file_in_pod" : f"oc exec {POD_NAME} touch content/{FILENAME_FOR_CREATE}",


    "run_ghost": f"oc exec {POD_NAME} -- node current/index.js --url={BLOG_URL}"
}
