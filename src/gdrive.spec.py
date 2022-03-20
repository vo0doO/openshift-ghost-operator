from webbrowser import get
from gdrive import *
import pickle
drive = get_service()
files_name = []


def loadMockData(path: str) -> object:
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data


d = get_files_id_for_delete(loadMockData("src/files.spec.pkl")["ids"])

def get_names(DRIVE, ids: list):
    if len(ids) == 0:
        return
    id = ids.pop()
    files_name.append(get_file_name(DRIVE, id))
    return get_names(DRIVE, ids)

get_names(drive, d)

s=""