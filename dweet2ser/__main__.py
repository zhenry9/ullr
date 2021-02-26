# import gevent.monkey; gevent.monkey.patch_all()
import argparse
import sys

from flask.globals import session

from . import utils, local_device, remote_device, webapp
from .webapp import views
from .cli import cli
from .session import DweetSession

current_session = DweetSession()

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

    if args.override:
        if args.override[0].upper() == "DTE":
            other_mode = "DCE"
        else:
            other_mode = "DTE"
        try:
            local = local_device.LocalDevice(args.override[1], args.override[0])
            remote = remote_device.RemoteDevice(args.override[2], other_mode)
            current_session.bus.add_device(local)
            current_session.bus.add_device(remote)
        except Exception as e:
            utils.print_to_ui(f"Override failed: {e}", sys=True)

    elif args.file:
        current_session.add_devices_from_file(args.file)

    elif not args.empty:
        current_session.add_devices_from_file()

    if args.nowebui:
        cli.init(current_session)
        utils.set_ui("cli")
        cli.menu()
    
    else:
        views.init(current_session)
        utils.set_ui("webapp")
        webapp.run()
    

if __name__ == "__main__":
    sys.exit(main())
