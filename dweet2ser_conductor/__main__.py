import sys

import time

from colorama import init as colorama_init
from termcolor import colored

from dweet2ser_conductor import remote_device, local_device, device_bus

# colorama call
colorama_init()

BUS = device_bus.DeviceBus()


def add_device():
    name = input("\nDevice Name: ")
    location = input("Location (1.local 2.remote): ")
    mode = input("Type (DCE/DTE): ").upper()
    d = None

    if location == "1":
        port = input("Port: ")
        try:
            d = local_device.LocalDevice(port, mode, name)
        except Exception as e:
            print(e)

    elif location == "2":
        thing_id = input("Thing ID: ")
        key = input("Thing Key: ")
        if key == "None" or key == "":
            key = None
        try:
            d = remote_device.RemoteDevice(thing_id, key, mode, name)
        except Exception as e:
            print(e)
    else:
        print("Invalid input")
        return
    if d:
        BUS.add_device(d)
    return


def remove_device():
    BUS.print_status()
    device = input("\nDevice to remove: ")
    BUS.remove_device(device)
    return


def process_input(cmd, ):
    if cmd == "info":
        return BUS.print_status()
    if cmd == "threads":
        return BUS.print_threads()
    if cmd == "add":
        return add_device()
    if cmd == "remove":
        return remove_device()
    else:
        # print command help
        print("\tType 'info' to display session info.\n"
              "\tType 'add' to add a device.\n"
              "\tType 'remove' to remove a device."
              )
        return


def idle():
    while True:
        time.sleep(1)


def main():
    print("\t\t*************************************************")
    print("\t\t**               " + colored("Dweet", "cyan") + " to " + colored("Serial", "red") + "               **")
    print("\t\t**                by Zach Henry                **")
    print("\t\t*************************************************")

    while True:
        cmd = ''
        try:
            cmd = input("\nType 'exit' to exit or ENTER for help.\n")
        except EOFError:  # if ran as a daemon, make sure we don't reach EOF prematurely
            idle()
        if cmd == 'exit':
            break
        process_input(cmd)
        time.sleep(.0001)


if __name__ == "__main__":
    sys.exit(main())
