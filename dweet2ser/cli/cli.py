import time

from ..local_device import LocalDevice
from ..remote_device import RemoteDevice
from .interface import s_input, s_print

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
            s_print(e)

    elif location == "2":
        thing_id = s_input("Thing ID: ")
        key = s_input("Thing Key: ")
        if key == "None" or key == "":
            key = None
        try:
            d = RemoteDevice(thing_id, mode, key, name, mute)
        except Exception as e:
            s_print(e)
    else:
        s_print("Invalid input")
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
        return s_print(current_session.bus.print_status())
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
        s_print("\tType 'info' to display session info.\n"
                "\tType 'add' to add a device.\n"
                "\tType 'remove' to remove a device.\n"
                "\tType 'save' to save the current configuration as default."
                )
        return


def idle():
    while True:
        time.sleep(1)

def menu():
    while True:
        cmd = ''
        try:
            time.sleep(.0001)
            cmd = s_input("\nType 'exit' to exit or ENTER for help.\n")
        except EOFError:  # if ran as a daemon, make sure we don't reach EOF prematurely
            idle()
        if cmd == 'exit':
            break
        process_input(cmd)
