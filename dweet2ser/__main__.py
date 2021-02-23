import argparse
import sys

from colorama import init as colorama_init
from termcolor import colored

from . import device_bus, local_device, remote_device, views, webapp
from .settings import print_to_web_console, sys_stamp
from .setup_config import Dweet2serConfiguration

colorama_init()

BUS = device_bus.DeviceBus()
CFG = Dweet2serConfiguration(BUS)

views.init(BUS, CFG)

def main():
    arg_parser = argparse.ArgumentParser(description="An interface for networking R232 devices using dweet.io.")
    options = arg_parser.add_mutually_exclusive_group()
    options.add_argument("--file", type=str, help="Specify config file to use, overriding defaults.")
    options.add_argument("--empty", action='store_true', help="Start dweet2ser with no devices. "
                                                              "Useful for fixing broken config files "
                                                              "or creating new ones.")
    options.add_argument("--override", metavar=('MODE', 'PORT', 'THING_NAME'), action="store", type=str, nargs=3,
                         help="Setup a basic connection with command line arguments."
                              "\ne.g. --override DCE /dev/ttyUSB0 dweet2ser_default.")
    args = arg_parser.parse_args()

    if args.override:
        if args.override[0].upper() == "DTE":
            other_mode = "DCE"
        else:
            other_mode = "DTE"
        try:
            local = local_device.LocalDevice(args.override[1], args.override[0])
            remote = remote_device.RemoteDevice(args.override[2], other_mode)
            BUS.add_device(local)
            BUS.add_device(remote)
        except Exception as e:
            print_to_web_console(f"{sys_stamp}Override failed: {e}")

    elif args.file:
        CFG.add_devices_from_file(args.file)

    elif not args.empty:
        CFG.add_devices_from_file()

    webapp.run()


if __name__ == "__main__":
    sys.exit(main())
