import datetime
import os
import uuid
import socket
import re
import sys
import glob
import serial
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
        return os.path.join(home_path, 'ullr', file_name)
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
        file_name = "ullr.log"
        path = os.path.join(home_path, 'ullr', file_name)
    else:
        path = USER_SPECIFIED_DEFAULT_CONFIG_FILE
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def setup_logger():
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    handler = logging.handlers.RotatingFileHandler(
        get_log_file(), maxBytes=(1024 * 100), backupCount=5
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
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
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(100)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
        for item in glob.glob('/dev/serial[0-9]*'):
            ports.append(item)
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def print_to_ui(message, endline="\n", sys=False):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    no_colors = ansi_escape.sub('', message)
    logger.info(no_colors)
    if sys:
        message = sys_stamp + message
    else:
        message = timestamp() + message
    if ui == "webapp":
        message = ansi_escape.sub('', message)
        socketing.print_to_web_console(message, endline=endline)
    elif ui == "cli":
        interface.s_print(message, end=endline)
