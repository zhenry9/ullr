import time

from ..local_device import LocalDevice
from ..remote_device import RemoteDevice
from ..utils import s_input, print_to_ui

current_session = object()

def init(session):
    global current_session
    current_session = session

def add_device():
    name = s_input("\nDevice Name: ")
    location = s_input("Location (1.local 2.remote): ")
    mode = s_input("Type (DCE/DTE): ").upper()
    mute = s_input("Mute device? (y/n): ")
    if mute.upper().strip() == "Y" or mute.upper().strip() == "YES":
        mute = True
    else:
        mute = False
    d = None

    if location == "1":
        port = s_input("Port: ")
        baudrate = s_input("Baudrate: ")
        if baudrate == "":
            baudrate = 9600
        try:
            d = LocalDevice(
                port=port, 
                mode=mode,
                name=name, 
                mute=mute, 
                baudrate=baudrate
                )
        except Exception as e:
            print_to_ui(e)

    elif location == "2":
        thing_id = s_input("Thing ID: ")
        key = s_input("Thing Key: ")
        if key == "None" or key == "":
            key = None
        try:
            d = RemoteDevice(thing_id, mode, key, name, mute)
        except Exception as e:
            print_to_ui(e)
    else:
        print_to_ui("Invalid input")
        return
    if d:
        current_session.bus.add_device(d)
    return


def remove_device():
    current_session.bus.print_status()
    device = s_input("\nDevice to remove: ")
    current_session.bus.remove_device(device)
    return


def process_input(cmd, ):
    if cmd == "info":
        return current_session.bus.print_status()
    if cmd == "threads":
        return current_session.bus.print_threads()
    if cmd == "add":
        return add_device()
    if cmd == "remove":
        return remove_device()
    if cmd == "save":
        return current_session.save_current_to_file()
    else:
        # print command help
        print_to_ui("\tType 'info' to display session info.\n"
                "\tType 'add' to add a device.\n"
                "\tType 'remove' to remove a device.\n"
                "\tType 'save' to save the current configuration as default."
                )
        return


def idle():
    while True:
        time.sleep(1)
