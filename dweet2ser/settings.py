import datetime
import os
import socket



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

CONFIG_COMMENTS = str("\n; The settings in the [DEFAULT] section reference the values set in 'settings.py' " +
                      "in the package directory." +
                      "\n; They should be here for config file stability." +
                      "\n; If you would like to change these default settings permanently, " +
                      "you should do so in settings.py, not here." +
                      "\n; Make sure you know what you're doing.\n\n")

# defaults when writing new configuration
CONFIG_DEFAULTS = {"type": "",
                   "location": "",
                   "port": "",
                   "thing_name": "dweet2ser_default",
                   "key": "None",
                   "mute": "False",
                   "baud": "9600"
                   }

sys_stamp = "[ sys ] "


def timestamp():
    return "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] "


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
