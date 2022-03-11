import logging
import subprocess
import time
import traceback
from msilib.schema import Error

logger = logging.getLogger(__name__)


def run(command):
    if not command:
        print()
        traceback.print_exc(100)
    try:
        result = subprocess.getoutput(f"{command}")
        return result
    except Exception as exc:
        logger.error("Error: ", exc.args)
        return exc

def runs(commands):
    if not commands:
        raise Error("Нет списка комманд")
    commands.reverse()
    results = []
    for cmd in commands: # FIXME: Рекурсия !
        try:
            result = run(cmd)
            results.append(result)
            time.sleep(1)
            continue
        except Exception as exc:
            logger.error(f"Error: ", exc.args)
