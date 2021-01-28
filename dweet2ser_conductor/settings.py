import datetime
import socket

from colorama import init as colorama_init, Fore, Style

colorama_init()

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
