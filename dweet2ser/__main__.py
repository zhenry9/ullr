import argparse
import queue
import sys

# 3rd party imports
import time

from colorama import init
from termcolor import colored

from dweet2ser import dweetsession
from dweet2ser import setup_config

# colorama call
init()

CONFIGURATION = setup_config.DweetConfiguration()
CFG = CONFIGURATION.parser
bucket = queue.Queue()


def setup():
    CONFIGURATION.setup()


def process_input(cmd, dweet_sesh):
    if cmd == "RESTART" or cmd == "restart":
        return bucket.put('crash', block=False)
    if cmd == "path":
        print(f"\tDefault config file: {CONFIGURATION.default_config_file}")
        path = CFG.get('User', 'user_config_file')
        if path == '':
            print("\tUser config file not found. Use 'setup' to create. Using defaults.")
        else:
            print(f"\tPath to user config file: {path}")
        return
    if cmd == "setup":
        CONFIGURATION.setup()
        return print("RESTART REQUIRED")
    if cmd == "info":
        return dweet_sesh.print_info()
    if cmd == "get":
        return dweet_sesh.write_last_dweet_to_serial()
    else:
        # print command help
        print("\tType 'info' to display session info.\n"
              "\tType 'get' to write the last message to serial, if it's available.\n"
              "\tType 'restart' to restart the listen thread.\n"
              "\tType 'path' to display paths to config files.\n"
              "\tType 'setup' to run the configuration setup."
              )
        return


def idle():
    while True:
        time.sleep(1)


def main():
    # start parsing CL arguments
    parser = argparse.ArgumentParser(description="An interface for connecting an RS232 port to dweet.io.")
    parser.add_argument('--port', '-p', type=str,
                        help='Manually specify port you are connecting to, overriding default e.g. COM7 or /dev/tty0')
    parser.add_argument('mode', type=str, choices=['DTE', 'DCE'],
                        help='Whether you are on the software side (DTE) or the device side (DCE) of the connection.',
                        default='DTE')

    args = parser.parse_args()
    dweet_sesh = dweetsession.DweetSession.from_config_parser(CFG, args.port, args.mode, bucket)

    dweet_sesh.start()

    print(colored("\n" + sys.argv[0] +
                  " running on port: " + dweet_sesh.port +
                  " in " + dweet_sesh.mode + " mode.\n", "red"))

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
        process_input(cmd, dweet_sesh)


if __name__ == "__main__":
    sys.exit(main())
