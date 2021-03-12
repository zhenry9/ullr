import time

from colorama import init as colorama_init
from termcolor import colored

from .. import __version__ as version
from ..local_device import LocalDevice
from ..remote_device import RemoteDevice
from . import interface

current_session = object()
colorama_init()


def init(session):
    global current_session
    current_session = session


def add_device():
    name = interface.s_input("\nDevice Name: ")
    location = interface.s_input("Location (1.local 2.remote): ")
    mode = interface.s_input("Type (DCE/DTE): ").upper()
    mute = interface.s_input("Mute device? (y/n): ")
    if mute.upper().strip() == "Y" or mute.upper().strip() == "YES":
        mute = True
    else:
        mute = False
    d = None

    if location == "1":
        port = interface.s_input("Port: ")
        baudrate = interface.s_input("Baudrate: ")
        if baudrate == "":
            baudrate = 9600
        try:
            d = LocalDevice(
                port=port,
                mode=mode,
                name=name,
                mute=mute,
                baudrate=int(baudrate)
            )
        except Exception as e:
            interface.s_print(e)

    elif location == "2":
        thing_id = interface.s_input("Thing ID: ")
        key = interface.s_input("Thing Key: ")
        if key == "None" or key == "":
            key = None
        try:
            d = RemoteDevice(thing_id, mode, key, name, mute)
        except Exception as e:
            interface.s_print(e)
    else:
        interface.s_print("Invalid input")
        return
    if d:
        current_session.bus.add_device(d)
    return


def remove_device():
    current_session.bus.print_status()
    device = interface.s_input("\nDevice to remove: ")
    current_session.bus.remove_device(device)
    return


def process_input(cmd, ):
    if cmd == "info":
        return interface.s_print(interface.get_devices_table(current_session))
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
        interface.s_print("\tType 'info' to display session info.\n"
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
            cmd = interface.s_input(
                "\nType 'exit' to exit or ENTER for help.\n")
        except EOFError:  # if ran as a daemon, make sure we don't reach EOF prematurely
            idle()
        if cmd == 'exit':
            break
        process_input(cmd)


def run():
    interface.s_print("\t\t*************************************************\n"
                      "\t\t**                   " + colored("dweet", "cyan") + "2" +
                      colored("ser", "red") + "                 **\n"
                      f"\t\t**                    v{version}                   **\n"
                      "\t\t*************************************************\n")
    menu()
