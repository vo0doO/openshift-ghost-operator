from asyncio import subprocess
import os
import sys
import time
import logging
import traceback
from uuid import uuid5
from msilib.schema import Error
import subprocess

logger = logging.getLogger(__name__)


def run_command(command):
    if not command:
        print()
        traceback.print_exc(100)
    try:
        result = subprocess.getoutput(f"{command}")
        logger.info(f"Success: {command}.")
        return result
    except Exception as exc:
        logger.error("Error: ", exc.args)
        return exc

def run_commands(cmds):
    if not cmds:
        raise Error("Нет списка комманд")
    cmds.reverse()
    results = []
    for cmd in cmds: # FIXME: Рекурсия !
        try:
            result = run_command(cmd)
            results.append(result)
            logger.info(f"Success {str()}")
            time.sleep(1)
            continue
        except Exception as exc:
            logger.error(f"Error on run {str(cmd)}", exc.args)


if __name__ == "__main__":
    run_run_command(sys.argv[1:])
