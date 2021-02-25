import os
from configparser import ConfigParser

from .local_device import LocalDevice
from .remote_device import RemoteDevice
from .settings import CONFIG_COMMENTS, CONFIG_DEFAULTS
from . import utils
from .webapp.socketing import print_to_web_console

class Dweet2serConfiguration(object):

    def __init__(self):
        self.parser = ConfigParser()
        self.bus = object()
        self.config_file = utils.get_default_config_file()

    def add_devices_from_file(self, file=None):
        """ Attempt to add devices from an arbitrary file. If no file is given the default file is used.

        """
        if file == None:
            file = self.config_file
        if self._load_config_file(file):
            try:
                self._add_devices()
            except Exception as exc:
                print_to_web_console(f"{utils.sys_stamp}Invalid config file format: {exc}")

    def _add_devices(self):
        devices = self.parser.sections()
        # make sure there is actually something in config
        if len(devices) > 0:
            print_to_web_console(f"{utils.sys_stamp}Loading devices from config.")
            for d in devices:
                name = d
                location = self.parser[d]["location"]
                dev_type = self.parser[d]["type"]
                if self.parser[d]["mute"].upper().strip() == "TRUE":
                    mute = True
                else:
                    mute = False
                if location == "local":
                    port = self.parser[d]["port"]
                    baudrate = int(self.parser[d]["baud"])
                    try:
                        dev = LocalDevice(port, dev_type, name, mute, baudrate)
                        self.bus.add_device(dev)
                        print_to_web_console(f"{utils.sys_stamp}Added {location} {dev_type} device '{name}' from config.")
                    except Exception as e:
                        print_to_web_console(f"{utils.sys_stamp}Failed to add device '{name}' from default config: {e}")
                elif location == "remote":
                    thing_name = self.parser[d]["thing_name"]
                    if self.parser[d]["key"] == "" or self.parser[d]["key"].lower().strip() == "none":
                        key = None
                    else:
                        key = self.parser[d]["key"]
                    try:
                        dev = RemoteDevice(thing_name, dev_type, key, name, mute)
                        self.bus.add_device(dev)
                        print_to_web_console(f"{utils.sys_stamp}Added {location} {dev_type} device '{name}' from config.")
                    except Exception as e:
                        print_to_web_console(f"{utils.sys_stamp}Failed to add device '{name}' from default config: {e}")
                else:
                    print_to_web_console(f"{utils.sys_stamp}Failed to add device '{name}' from default config: "
                            f"invalid location '{location}'")

    def save_current_to_file(self):
        """ Save the current device bus to default config file

        """
        self.parser = ConfigParser()  # clear any settings in the parser
        self._add_defaults_to_parser()

        # add DCE settings to parser
        for dev in self.bus.dce_devices:
            self.parser.add_section(dev.name)
            self.parser[dev.name]["type"] = "DCE"
            if type(dev).__name__ == "LocalDevice":
                self.parser[dev.name]["location"] = "local"
                self.parser[dev.name]["port"] = dev.port_name
                self.parser[dev.name]["baud"] = dev.baudrate
            if type(dev).__name__ == "RemoteDevice":
                self.parser[dev.name]["location"] = "remote"
                self.parser[dev.name]["thing_name"] = dev.thing_id
                self.parser[dev.name]["key"] = str(dev.thing_key)
            self.parser[dev.name]["mute"] = str(dev.mute)

        # add DTE settings to parser
        for dev in self.bus.dte_devices:
            self.parser.add_section(dev.name)
            self.parser[dev.name]["type"] = "DTE"
            if type(dev).__name__ == "LocalDevice":
                self.parser[dev.name]["location"] = "local"
                self.parser[dev.name]["port"] = dev.port_name
                self.parser[dev.name]["baud"] = str(dev.baudrate)
            if type(dev).__name__ == "RemoteDevice":
                self.parser[dev.name]["location"] = "remote"
                self.parser[dev.name]["thing_name"] = dev.thing_id
                self.parser[dev.name]["key"] = str(dev.thing_key)
            self.parser[dev.name]["mute"] = str(dev.mute)

        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

        with open(self.config_file, 'w') as configfile:
            configfile.write(CONFIG_COMMENTS)
        with open(self.config_file, 'a') as configfile:
            self.parser.write(configfile)

        print_to_web_console(f"{utils.sys_stamp}Settings saved to config file: {self.config_file}")

    def _load_config_file(self, file):
        if not os.path.isabs(file):
            file = os.path.join(os.getcwd(), file)
        if os.path.exists(file):
            print_to_web_console(f"{utils.sys_stamp}Found config file at {file}.")
            try:
                self.parser = ConfigParser()
                self.parser.read(file)
                self._add_defaults_to_parser()
                return True
            except Exception as e:
                print_to_web_console(f"{utils.sys_stamp}Failed to read config file: {e}")
                return False

        else:
            self._add_defaults_to_parser()
            print_to_web_console(f"Config file {file} not found.")
            if file == self.config_file:
                print_to_web_console(f"{utils.sys_stamp}Creating empty default file at: {file}")
                self.save_current_to_file()
            return False

    def _add_defaults_to_parser(self):
        for item in CONFIG_DEFAULTS:
            if not self.parser.has_option("DEFAULT", item):
                self.parser["DEFAULT"][item] = CONFIG_DEFAULTS[item]
