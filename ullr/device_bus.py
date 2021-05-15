import threading
import time
from serial import SerialException

from colorama import Fore, Style
from colorama import init as colorama_init
from termcolor import colored
from urllib3.exceptions import ProtocolError

from .utils import internet_connection, print_to_ui, logger
from .webapp.socketing import print_tape, TAPES
from . import skiracetiming

colorama_init()

class DeviceBus(object):
    """
    Holds all the devices in a connection and facilitates communication between them. All DCE devices
    write to all DTE devices and vice versa.
    """

    def __init__(self):
        self.dce_devices = []
        self.dte_devices = []
        self.listen_threads = {}


    def add_device(self, device):
        """
        Adds the given device to the connection, and starts a listening thread if the device is not muted.
        """
        if device.mode == "DTE":
            self.dte_devices.append(device)
        if device.mode == "DCE":
            self.dce_devices.append(device)
        if not device.mute:
            self.listen_threads[device.name] = threading.Thread(
                target=self._listen_stream, args=[device])
            self.listen_threads[device.name].daemon = True
            self.listen_threads[device.name].start()
        print_to_ui(f"Added device {device.name}.")
        return True

    def find_device(self, key):
        for d in self.dce_devices:
            if d.name == key:
                return d
            elif str(d.sku) == key:
                return d
        for d in self.dte_devices:
            if d.name == key:
                return d
            elif str(d.sku) == key:
                return d
        return None

    def remove_device(self, name_or_sku):
        """
        Takes a device name, and removes that device if the name is found
        """
        device = self.find_device(name_or_sku)

        if device:
            device.kill_listen_stream()
            if device.mode.lower() == "dce":
                self.dce_devices.remove(device)
            elif device.mode.lower() == "dte":
                self.dte_devices.remove(device)
            TAPES.pop(device.sku, "")
            print_to_ui(f"Device '{device.name}' removed.")

        else:
            print_to_ui(f"Device {name_or_sku} not found.")

    def update_translation(self, name_or_sku, translation_list):
        device = self.find_device(name_or_sku)
        if device:
            try:
                device.translation = translation_list
                print_to_ui(
                    f"Updated translation for {device.name}: {translation_list}")
            except Exception as e:
                print_to_ui(
                    f"Could not update translation for {device.name}: {e}")
        else:
            print_to_ui(f"Device {name_or_sku} not found.")

    def print_threads(self):
        print_to_ui(self.listen_threads)

    def _listen_stream(self, device):
        """
        Listens for messages from the given device, then writes to all appropriate devices on bus.
        """
        print_to_ui(f"Listen stream started for {device.name}.")

        while device.listening:
            try:
                message = device.message_queue.get()
                try:
                    message_decoded = message.decode('latin-1').rstrip().replace('\r', '')
                except ValueError as e:
                    logger.warn(f"Received non-bytes message: {message}")
                    print_to_ui(f"{message}: {e}")
                    message_decoded = "<indecipherable>"

                print_tape(device.sku, message_decoded)
                print_to_ui(f"Received {colored(device.type, device.type_color)} message from {device.name}:"
                            f" {Fore.LIGHTWHITE_EX}{message_decoded}{Style.RESET_ALL}")

                if device.translation[0]:
                    try:
                        message_decoded = skiracetiming.translate(message_decoded, device.translation[1],
                                                                    device.translation[2], device.translation[3])
                        message = message_decoded.encode()
                        message_decoded = message_decoded.rstrip().replace('\r', '')
                        print_to_ui(f"Translated from {device.translation[1]} to {device.translation[2]} "
                                    f"with channel shift {device.translation[3]}.")

                    except Exception as e:
                        print_to_ui(f"Translation failed: {e}")

                def write_to_device_list(list):
                    for d in list:
                        if d.accepts_incoming:
                            if d.write(message):
                                print_to_ui(
                                    f"{colored(d.type.capitalize(), d.type_color)} message sent to {d.name}: "
                                    f"{message_decoded}")
                            else:
                                print_to_ui(f"Writing to {d.name} failed.")

                if device.mode == "DTE":
                    # Messages from DTE devices get sent to all DCE devices.
                    write_to_device_list(self.dce_devices)

                elif device.mode == "DCE":
                    # Messages from DCE devices get sent to all DTE devices.
                    write_to_device_list(self.dte_devices)

                else:
                    print_to_ui("Mode not found")
                    
            except SerialException as e:
                print_to_ui(f"{e}")
                print_to_ui(f"{device.name} unplugged. Removing device.")
                self.remove_device(device.name)

        return True


