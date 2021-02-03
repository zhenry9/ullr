import os
from configparser import ConfigParser

from dweet2ser.local_device import LocalDevice
from dweet2ser.remote_device import RemoteDevice
from dweet2ser.settings import sys_stamp, CONFIG_DEFAULTS, DEFAULT_CONFIG_FILE, s_print


class Dweet2serConfiguration(object):

    def __init__(self, bus):
        self.parser = ConfigParser()
        self.bus = bus

    def add_devices_from_file(self, file=DEFAULT_CONFIG_FILE):
        """ Attempt to add devices from an arbitrary file. If no file is given the default file is used.

        """
        if self._load_config_file(file):
            try:
                self._add_devices()
            except Exception as exc:
                s_print(f"{sys_stamp}Invalid config file format: {exc}")

    def _add_devices(self):
        devices = self.parser.sections()
        # make sure there is actually something in config
        if len(devices) > 0:
            s_print(f"{sys_stamp}Loading devices from config.")
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
                        s_print(f"{sys_stamp}Added {location} {dev_type} device '{name}' from config.")
                    except Exception as e:
                        s_print(f"{sys_stamp}Failed to add device '{name}' from default config: {e}")
                elif location == "remote":
                    thing_name = self.parser[d]["thing_name"]
                    if self.parser[d]["key"] == "" or self.parser[d]["key"].lower().strip() == "none":
                        key = None
                    else:
                        key = self.parser[d]["key"]
                    try:
                        dev = RemoteDevice(thing_name, dev_type, key, name, mute)
                        self.bus.add_device(dev)
                        s_print(f"{sys_stamp}Added {location} {dev_type} device '{name}' from config.")
                    except Exception as e:
                        s_print(f"{sys_stamp}Failed to add device '{name}' from default config: {e}")
                else:
                    s_print(f"{sys_stamp}Failed to add device '{name}' from default config: "
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
            self.parser[dev.name]["mute"] = str(dev.mute)

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
            self.parser[dev.name]["mute"] = str(dev.mute)

        os.makedirs(os.path.dirname(DEFAULT_CONFIG_FILE), exist_ok=True)

        with open(DEFAULT_CONFIG_FILE, 'w') as configfile:
            configfile.write("\n; The settings in the [DEFAULT] section reference the values set in 'settings.py' "
                             "in the package directory."
                             "\n; They should be here for config file stability."
                             "\n; If you would like to change these default settings permanently, "
                             "you should do so in settings.py, not here."
                             "\n; Make sure you know what you're doing.\n\n")
        with open(DEFAULT_CONFIG_FILE, 'a') as configfile:
            self.parser.write(configfile)

        s_print(f"{sys_stamp}Settings saved to config file: {DEFAULT_CONFIG_FILE}")

    def _load_config_file(self, file):
        if not os.path.isabs(file):
            file = os.path.join(os.getcwd(), file)
        if os.path.exists(file):
            s_print(f"{sys_stamp}Found config file at {file}.")
            try:
                self.parser = ConfigParser()
                self.parser.read(file)
                return True
            except Exception as e:
                s_print(f"{sys_stamp}Failed to read config file: {e}")
                return False

        else:
            self._add_defaults_to_parser()
            s_print(f"{sys_stamp}Config file {file} not found.")
            if file == DEFAULT_CONFIG_FILE:
                s_print(f"{sys_stamp}Creating empty default file at: {file}")
                os.makedirs(os.path.dirname(DEFAULT_CONFIG_FILE), exist_ok=True)
                with open(DEFAULT_CONFIG_FILE, 'w') as configfile:
                    self.parser.write(configfile)
            return False

    def _add_defaults_to_parser(self):
        self.parser["DEFAULT"] = CONFIG_DEFAULTS
