import time

from . import cli
from ..utils import s_input

def run():
    while True:
        cmd = ''
        try:
            time.sleep(.0001)
            cmd = s_input("\nType 'exit' to exit or ENTER for help.\n")
        except EOFError:  # if ran as a daemon, make sure we don't reach EOF prematurely
            cli.idle()
        if cmd == 'exit':
            break
        cli.process_input(cmd)