import os
from configparser import ConfigParser

from .local_device import LocalDevice
from .remote_device import RemoteDevice
from .device_bus import DeviceBus
from .settings import CONFIG_COMMENTS, CONFIG_DEFAULTS
from . import utils


class Dweet2serConfiguration(object):

    def __init__(self):
        self.parser = ConfigParser()
        self.bus = DeviceBus()
        self.config_file = utils.get_default_config_file()

    def add_devices_from_file(self, file=None):
        """ Attempt to add devices from an arbitrary file. If no file is given
            the default file is used.

        """
        if file is None:
            file = self.config_file
        if self._load_config_file(file):
            try:
                self._add_devices()
            except Exception as exc:
                utils.print_to_ui(
                    f"Invalid config file format: {exc}", sys=True)

    def _add_devices(self):
        devices = self.parser.sections()
        # make sure there is actually something in config
        if len(devices) > 0:
            utils.print_to_ui(f"Loading devices from config...", sys=True)
            for d in devices:
                name = d
                translation = [False, None, None, 0]
                location = self.parser[d]["location"]
                dev_type = self.parser[d]["type"]
                if self.parser[d]["mute"].upper().strip() == "TRUE":
                    mute = True
                else:
                    mute = False
                if self.parser[d]["translated"].upper().strip() == "TRUE":
                    translation[0] = True
                    translation[1] = self.parser[d]["translated_from"]
                    translation[2] = self.parser[d]["translated_to"]
                    translation[3] = int(self.parser[d]["channel_shift"])
                if location == "local":
                    port = self.parser[d]["port"]
                    baudrate = int(self.parser[d]["baud"])
                    try:
                        dev = LocalDevice(
                            port=port,
                            mode=dev_type,
                            name=name,
                            mute=mute,
                            baudrate=baudrate,
                            translation=translation)
                        self.bus.add_device(dev)
                        utils.print_to_ui(
                            f"Added {location} {dev_type} device '{name}' from config.", sys=True)
                    except Exception as e:
                        utils.print_to_ui(
                            f"Failed to add device '{name}' from default config: {e}", sys=True)
                elif location == "remote":
                    thing_name = self.parser[d]["thing_name"]
                    if self.parser[d]["key"] == "" or self.parser[d]["key"].lower().strip() == "none":
                        key = None
                    else:
                        key = self.parser[d]["key"]
                    try:
                        dev = RemoteDevice(
                            thing_id=thing_name,
                            mode=dev_type,
                            thing_key=key,
                            name=name,
                            mute=mute,
                            translation=translation)
                        self.bus.add_device(dev)
                        utils.print_to_ui(
                            f"Added {location} {dev_type} device '{name}' from config.", sys=True)
                    except Exception as e:
                        utils.print_to_ui(
                            f"Failed to add device '{name}' from default config: {e}", sys=True)
                else:
                    utils.print_to_ui(f"Failed to add device '{name}' from default config: "
                                      f"invalid location '{location}'", sys=True)

    def save_current_to_file(self):
        """ Save the current device bus to default config file

        """
        self.parser = ConfigParser()  # clear any settings in the parser
        self._add_defaults_to_parser()

        def add_device_to_config(dev):
            if type(dev).__name__ == "LocalDevice":
                self.parser[dev.name]["location"] = "local"
                self.parser[dev.name]["port"] = dev.port_name
                self.parser[dev.name]["baud"] = str(dev.baudrate)
            if type(dev).__name__ == "RemoteDevice":
                self.parser[dev.name]["location"] = "remote"
                self.parser[dev.name]["thing_name"] = dev.thing_id
                self.parser[dev.name]["key"] = str(dev.thing_key)
            self.parser[dev.name]["mute"] = str(dev.mute)
            self.parser[dev.name]["translated"] = str(dev.translation[0])
            self.parser[dev.name]["translated_from"] = str(dev.translation[1])
            self.parser[dev.name]["translated_to"] = str(dev.translation[2])
            self.parser[dev.name]["channel_shift"] = str(dev.translation[3])

        # add DCE settings to parser
        for dev in self.bus.dce_devices:
            self.parser.add_section(dev.name)
            self.parser[dev.name]["type"] = "DCE"
            add_device_to_config(dev)

        # add DTE settings to parser
        for dev in self.bus.dte_devices:
            self.parser.add_section(dev.name)
            self.parser[dev.name]["type"] = "DTE"
            add_device_to_config(dev)

        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

        with open(self.config_file, 'w') as configfile:
            configfile.write(CONFIG_COMMENTS)
        with open(self.config_file, 'a') as configfile:
            self.parser.write(configfile)

        utils.print_to_ui(
            f"Settings saved to config file: {self.config_file}", sys=True)

    def _load_config_file(self, file):
        if not os.path.isabs(file):
            file = os.path.join(os.getcwd(), file)
        if os.path.exists(file):
            utils.print_to_ui(f"Found config file at {file}.", sys=True)
            try:
                self.parser = ConfigParser()
                self.parser.read(file)
                self._add_defaults_to_parser()
                return True
            except Exception as e:
                utils.print_to_ui(f"Failed to read config file: {e}", sys=True)
                return False

        else:
            self._add_defaults_to_parser()
            utils.print_to_ui(f"Config file {file} not found.", sys=True)
            if file == self.config_file:
                utils.print_to_ui(
                    f"Creating empty default file at: {file}", sys=True)
                self.save_current_to_file()
            return False

    def _add_defaults_to_parser(self):
        for item in CONFIG_DEFAULTS:
            if not self.parser.has_option("DEFAULT", item):
                self.parser["DEFAULT"][item] = CONFIG_DEFAULTS[item]
