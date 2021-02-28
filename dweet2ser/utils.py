import datetime
import os
import socket
import re
import logging
import logging.handlers

from colorama import Fore, Style
from colorama import init as colorama_init

from .settings import USER_SPECIFIED_DEFAULT_CONFIG_FILE, USER_SPECIFIED_LOG_FILE
from .webapp import socketing
from .cli import interface

colorama_init()
ui = "webapp"

def set_ui(user_int):
    global ui
    ui = user_int

def get_default_config_file():
    if USER_SPECIFIED_DEFAULT_CONFIG_FILE is None:
        home_path = os.path.expanduser('~')
        # check if we're on linux running as superuser, then choose more appropriate directory
        if home_path == "/root":
            home_path = "/etc"
        else:
            home_path = os.path.join(home_path, '.config')
        file_name = "config.ini"
        return os.path.join(home_path, 'dweet2ser', file_name)
    else:
        return USER_SPECIFIED_DEFAULT_CONFIG_FILE

def get_log_file():
    if USER_SPECIFIED_LOG_FILE is None:
        home_path = os.path.expanduser('~')
        # check if we're on linux running as superuser, then choose more appropriate directory
        if home_path == "/root":
            home_path = "/var/log"
        else:
            home_path = os.path.join(home_path, '.log')
        file_name = "dweet2ser.log"
        path = os.path.join(home_path, 'dweet2ser', file_name)
    else:
        path = USER_SPECIFIED_DEFAULT_CONFIG_FILE
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

def setup_logger():
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
        get_log_file(), maxBytes=(1024 * 100), backupCount=5
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logger()

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

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_available_com_ports():
    names = []
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        names.append(p[0])
    return names

def print_to_ui(message, endline="\n", sys=False):
    logger.info(message)
    if sys:
        message = sys_stamp + message
    else:
        message = timestamp() + message
    if ui == "webapp":
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        no_colors = ansi_escape.sub('', message)
        socketing.print_to_web_console(no_colors, endline=endline)
    elif ui == "cli":
        interface.s_print(message, end=endline)

