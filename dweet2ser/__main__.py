# import gevent.monkey; gevent.monkey.patch_all()
import argparse
import sys

from . import local_device, remote_device, webapp, cli
from .utils import sys_stamp
from .webapp import views
from .webapp.socketing import print_to_web_console
from .session import DweetSession

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
    arg_parser.add_argument("--nowebui", action="store_true", help="Use dweet2ser from the command line."
                                                                   "Don't run GUI on webserver.")                          
    args = arg_parser.parse_args()

    session = DweetSession()

    if args.override:
        if args.override[0].upper() == "DTE":
            other_mode = "DCE"
        else:
            other_mode = "DTE"
        try:
            local = local_device.LocalDevice(args.override[1], args.override[0])
            remote = remote_device.RemoteDevice(args.override[2], other_mode)
            session.bus.add_device(local)
            session.bus.add_device(remote)
        except Exception as e:
            print_to_web_console(f"{sys_stamp}Override failed: {e}")

    elif args.file:
        session.add_devices_from_file(args.file)

    elif not args.empty:
        session.add_devices_from_file()

    if args.nowebui:
        session.ui = "cli"
        cli.run(session)
    else:
        views.init(session)
        webapp.run()
    

if __name__ == "__main__":
    sys.exit(main())
