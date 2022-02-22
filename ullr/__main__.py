# import gevent.monkey; gevent.monkey.patch_all()
import argparse
import sys
import os

from . import __version__ as version
from . import local_device, remote_device, utils, webapp
from .cli import cli
from .session import Session
from .webapp import views

current_session = Session()

# turn off console output if run as windows GUI
if sys.executable.endswith("pythonw.exe"):
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.path.join(os.getenv("TEMP"), "stderr-"+os.path.basename(sys.argv[0])), "w")


def main():
    arg_parser = argparse.ArgumentParser(
        description="An interface for networking R232 devices using dweet.io.")
    options = arg_parser.add_mutually_exclusive_group()
    options.add_argument(
        "--file", type=str, help="Specify config file to use, overriding defaults.")
    options.add_argument("--empty", action='store_true', help="Start Ullr with no devices. "
                                                              "Useful for fixing broken config files "
                                                              "or creating new ones.")
    options.add_argument("--override", metavar=('MODE', 'PORT', 'THING_NAME'), action="store", type=str, nargs=3,
                         help="Setup a basic connection with command line arguments."
                              "\ne.g. --override DCE /dev/ttyUSB0 Ullr_default.")
    arg_parser.add_argument("--nowebui", action="store_true", help="Use Ullr from the command line."
                                                                   "Don't run GUI on webserver.")
    arg_parser.add_argument("--uiport", type=int,
                            default=5000, help="Port for web interface.")
    arg_parser.add_argument("--nopopup", action="store_true",
                            help="Disable automatic opening of browser window to web interface on run.")
    args = arg_parser.parse_args()

    utils.print_to_ui(f"Starting Ullr v{version}...", sys=True)

    if args.override:
        if args.override[0].upper() == "DTE":
            other_mode = "DCE"
        else:
            other_mode = "DTE"
        try:
            local = local_device.LocalDevice(
                args.override[1], args.override[0])
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
        cli.run()

    else:
        views.init(current_session)
        utils.set_ui("webapp")
        webapp.run(port=args.uiport, nopopup=args.nopopup)


if __name__ == "__main__":
    main()
