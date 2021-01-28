import os
from configparser import ConfigParser

from local_device import LocalDevice
from remote_device import RemoteDevice
from settings import sys_stamp, CONFIG_DEFAULTS


class Dweet2serConfiguration(object):

    def __init__(self, bus):
        self.parser = ConfigParser()
        self.bus = bus
        home_path = os.path.expanduser('~')
        # check if we're on linux running as superuser, then choose more appropriate directory
        if home_path == "/root":
            home_path = "/etc"
        else:
            home_path = os.path.join(home_path, '.config')
        file_name = "config.ini"
        self.default_config_file = os.path.join(home_path, 'dweet2ser', file_name)

    def add_devices_from_default(self):
        """ Attempt to add all the devices listed in the default config.ini file.

        """
        if self._load_config_file(self.default_config_file):
            self._add_devices()

    def add_devices_from_file(self, file):
        """ Attempt to add devices from an arbitrary file

        """
        if self._load_config_file(file):
            try:
                self._add_devices()
            except Exception as exc:
                print(f"{sys_stamp}Invalid config file format: {exc}")

    def _add_devices(self):
        devices = self.parser.sections()
        # make sure there is actually something in config
        if len(devices) > 0:
            print(f"{sys_stamp}Loading devices from config.")
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
                    try:
                        dev = LocalDevice(port, dev_type, name, mute)
                        self.bus.add_device(dev)
                        print(f"{sys_stamp}Added {location} {dev_type} device '{name}' from config.")
                    except Exception as e:
                        print(f"{sys_stamp}Failed to add device '{name}' from default config: {e}")
                elif location == "remote":
                    thing_name = self.parser[d]["thing_name"]
                    if self.parser[d]["key"] == "" or self.parser[d]["key"].lower().strip() == "none":
                        key = None
                    else:
                        key = self.parser[d]["key"]
                    try:
                        dev = RemoteDevice(thing_name, key, dev_type, name, mute)
                        self.bus.add_device(dev)
                        print(f"{sys_stamp}Added {location} {dev_type} device '{name}' from config.")
                    except Exception as e:
                        print(f"{sys_stamp}Failed to add device '{name}' from default config: {e}")
                else:
                    print(f"{sys_stamp}Failed to add device '{name}' from default config: "
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
            if type(dev).__name__ == "RemoteDevice":
                self.parser[dev.name]["location"] = "remote"
                self.parser[dev.name]["thing_name"] = dev.thing_id
                self.parser[dev.name]["key"] = str(dev.thing_key)

        # add DTE settings to parser
        for dev in self.bus.dte_devices:
            self.parser.add_section(dev.name)
            self.parser[dev.name]["type"] = "DTE"
            if type(dev).__name__ == "LocalDevice":
                self.parser[dev.name]["location"] = "local"
                self.parser[dev.name]["port"] = dev.port_name
            if type(dev).__name__ == "RemoteDevice":
                self.parser[dev.name]["location"] = "remote"
                self.parser[dev.name]["thing_name"] = dev.thing_id
                self.parser[dev.name]["key"] = str(dev.thing_key)

        os.makedirs(os.path.dirname(self.default_config_file), exist_ok=True)

        with open(self.default_config_file, 'w') as configfile:
            configfile.write("\n; The settings in the [DEFAULT] section reference the vaules set in 'settings.py' "
                             "in the package directory."
                             "\n; They should be here for config file stability."
                             "\n; If you would like to change these default settings permanently, "
                             "you should do so in settings.py, not here."
                             "\n; Make sure you know what you're doing.\n\n")
        with open(self.default_config_file, 'a') as configfile:
            self.parser.write(configfile)

        print(f"{sys_stamp}Settings saved to config file: {self.default_config_file}")

    def _load_config_file(self, file):
        if os.path.exists(file):
            print(f"{sys_stamp}Found config file at {file}.")
            try:
                self.parser = ConfigParser()
                self.parser.read(file)
                return True
            except Exception as e:
                print(f"{sys_stamp}Failed to read config file: {e}")
                return False

        else:
            self._add_defaults_to_parser()
            print(f"{sys_stamp}Config file {file} not found.")
            if file == self.default_config_file:
                print(f"{sys_stamp}Creating empty default file at: {file}")
                os.makedirs(os.path.dirname(self.default_config_file), exist_ok=True)
                with open(self.default_config_file, 'w') as configfile:
                    self.parser.write(configfile)
            return False

    def _add_defaults_to_parser(self):
        self.parser["DEFAULT"] = CONFIG_DEFAULTS
