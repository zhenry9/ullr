import os
from configparser import ConfigParser
import uuid
import time

from .getmac import get_mac_address
from .local_device import LocalDevice
from .remote_device import RemoteDevice
from .device_bus import DeviceBus
from .settings import CONFIG_COMMENTS, CONFIG_DEFAULTS
from . import utils, mqtt_client


class UllrConfiguration(object):

    def __init__(self):
        self.parser = ConfigParser()
        self.bus = DeviceBus()
        self.config_file = utils.get_default_config_file()
        self.save_client_id = True

    def _get_client_id(self):
        try:
            CLIENT_ID = get_mac_address().replace(":", "")
        except:
            time.sleep(1)
            utils.logger.warn("getmac process failed. Falling back on uuid.getnode().")
            CLIENT_ID = hex(uuid.getnode())[2:]
            self.save_client_id = False
        return CLIENT_ID

    def add_devices_from_file(self, file=None):
        """ Attempt to add devices from an arbitrary file. If no file is given
            the default file is used.

        """
        if file is None:
            file = self.config_file
        if self._load_config_file(file):
            try:
                self._connect_to_mqtt_broker()
            except Exception as exc:
                utils.print_to_ui(f"Unable to connect to MQTT broker: {exc}")
            try:
                self._add_devices()
            except Exception as exc:
                utils.print_to_ui(
                    f"Invalid config file format: {exc}", sys=True)

    def _connect_to_mqtt_broker(self):
        section = self.parser["$mqtt"]
        broker_url = section["mqtt_broker_url"]
        broker_port = int(section["mqtt_broker_port"])
        broker_user = section["mqtt_broker_user"]
        broker_pw = section["mqtt_broker_pw"]
        client_id = section.get("client_id")
        if not client_id:
            client_id = self._get_client_id()
        mqtt_client.start_client(broker_url, broker_port, broker_user, broker_pw, client_id)

    def _add_devices(self):
        devices = self.parser.sections()
        # make sure there is actually something in config
        if len(devices) > 0:
            utils.print_to_ui(f"Loading devices from config...", sys=True)
            for d in devices:
                name = d
                if name[0] != "$":
                    translation = [False, None, None, 0]
                    location = self.parser[d]["location"]
                    dev_type = self.parser[d]["type"]
                    if self.parser[d]["mute"].upper().strip() == "TRUE":
                        mute = True
                    else:
                        mute = False
                    if self.parser[d]["published"].upper().strip() == "TRUE":
                        published = True
                    else:
                        published = False
                    if self.parser[d]["accepts_incoming"].upper().strip() == "FALSE":
                        accepts_incoming = False
                    else:
                        accepts_incoming = True
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
                                accepts_incoming=accepts_incoming,
                                baudrate=baudrate,
                                published=published,
                                translation=translation)
                            self.bus.add_device(dev)
                            utils.print_to_ui(
                                f"Added {location} {dev_type} device '{name}' from config.", sys=True)
                        except Exception as e:
                            utils.print_to_ui(
                                f"Failed to add device '{name}' from default config: {e}", sys=True)
                    elif location == "remote":
                        # backwards compatibility for previous versions that used Dweet backend with thing names
                        if self.parser[d].get("thing_name"):
                            topic_name = self.parser[d].get("thing_name")
                        else:
                            topic_name = self.parser[d].get("topic_name") 

                        on_time_max = int(self.parser[d].get("on_time_max"))   
                        try:
                            dev = RemoteDevice(
                                topic_name=topic_name,
                                mode=dev_type,
                                mute=mute,
                                accepts_incoming=accepts_incoming,
                                name=name,
                                on_time_max=on_time_max,
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
                self.parser[dev.name]["published"] = str(dev.published)
            if type(dev).__name__ == "RemoteDevice":
                self.parser[dev.name]["location"] = "remote"
                self.parser[dev.name]["topic_name"] = dev.topic_name
                self.parser[dev.name]["on_time_max"] = str(dev.on_time_max)
            self.parser[dev.name]["mute"] = str(dev.mute)
            self.parser[dev.name]["accepts_incoming"] = str(dev.accepts_incoming)
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

        # add MQTT settings to parser
        self.parser["$mqtt"]["mqtt_broker_url"] = mqtt_client.mqtt_broker_url
        self.parser["$mqtt"]["mqtt_broker_port"] = str(mqtt_client.mqtt_broker_port)
        self.parser["$mqtt"]["mqtt_broker_user"] = mqtt_client.mqtt_broker_user
        self.parser["$mqtt"]["mqtt_broker_pw"] = mqtt_client.mqtt_broker_pw
        if self.save_client_id:
            self.parser["$mqtt"]["client_id"] = mqtt_client.CLIENT_ID

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
            try:
                self._connect_to_mqtt_broker()
            except Exception as exc:
                utils.print_to_ui(f"Unable to connect to MQTT broker: {exc}")
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
        if not self.parser.has_section("$mqtt"):
            self.parser.add_section("$mqtt")
