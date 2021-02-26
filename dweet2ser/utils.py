import datetime
import logging
import os
import socket
import re
from threading import Lock

from colorama import Fore, Style
from colorama import init as colorama_init

from .settings import USER_SPECIFIED_DEFAULT_CONFIG_FILE
from . import webapp
from .webapp import socketing

colorama_init()


s_print_lock = Lock()
ui = "webapp"

def start_ui(user_int):
    global ui
    ui = user_int
    if ui == "webapp":
        webapp.run()
    elif ui == "cli":
        cli.run()

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

def get_available_com_ports():
    names = []
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        names.append(p[0])
    return names

def print_to_ui(message, endline="\n", sys=False):
    # logging stuff here
    if sys:
        message = sys_stamp + message
    else:
        message = timestamp() + message
    if ui == "webapp":
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        no_colors = ansi_escape.sub('', message)
        socketing.print_to_web_console(no_colors, endline=endline)
    elif ui == "cli":
        s_print(message, endline=endline)

def s_print(*a, **b):
    """Thread safe print function"""
    with s_print_lock:
        print(*a, **b)


def s_input(*a):
    """Thread safe input function"""
    with s_print_lock:
        print(*a, end='')
    return input('')
