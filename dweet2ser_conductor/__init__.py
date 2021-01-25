__version__ = '0.0.1'

import datetime

from colorama import init as colorama_init, Fore, Style

colorama_init()


def timestamp():
    return Fore.LIGHTBLACK_EX + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + Style.RESET_ALL + ": "
