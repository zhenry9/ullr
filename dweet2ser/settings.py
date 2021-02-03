import datetime
import os
import socket
from threading import Lock

from colorama import init as colorama_init, Fore, Style

colorama_init()

s_print_lock = Lock()


def _get_default_config_file():
    home_path = os.path.expanduser('~')
    # check if we're on linux running as superuser, then choose more appropriate directory
    if home_path == "/root":
        home_path = "/etc"
    else:
        home_path = os.path.join(home_path, '.config')
    file_name = "config.ini"
    return os.path.join(home_path, 'dweet2ser', file_name)


DEFAULT_CONFIG_FILE = _get_default_config_file()

# defaults when writing new configuration
CONFIG_DEFAULTS = {"type": "",
                   "location": "",
                   "port": "",
                   "thing_name": "dweet2ser_default",
                   "key": "None",
                   "mute": "False"
                   }

sys_stamp = "[ " + Fore.LIGHTBLACK_EX + "sys" + Style.RESET_ALL + " ] "


def timestamp():
    return "[" + Fore.LIGHTBLACK_EX + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + Style.RESET_ALL + "] "


def internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        #  print(ex)
        return False


def s_print(*a, **b):
    """Thread safe print function"""
    with s_print_lock:
        print(*a, **b)


def s_input(*a):
    """Thread safe input function"""
    with s_print_lock:
        print(*a, end='')
    return input('')
