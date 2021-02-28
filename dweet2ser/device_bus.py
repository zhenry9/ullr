import threading
import time

from colorama import Fore, Style
from colorama import init as colorama_init
from termcolor import colored

from .utils import internet_connection, print_to_ui
from .webapp.socketing import print_tape

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

        self.stream_restarter = threading.Thread(target=self._check_for_crashed_threads)
        self.stream_restarter.daemon = True
        self.stream_restarter.start()

    def add_device(self, device):
        """
        Adds the given device to the connection, and starts a listening thread if the device is not muted.
        """
        if device.mode == "DTE":
            self.dte_devices.append(device)
        if device.mode == "DCE":
            self.dce_devices.append(device)
        if not device.mute:
            self.listen_threads[device.name] = threading.Thread(target=self._listen_stream, args=[device])
            self.listen_threads[device.name].daemon = True
            self.listen_threads[device.name].start()
        return True

    def remove_device(self, device_name):
        """
        Takes a device name, and removes that device if the name is found
        """
        found = False
        for d in self.dce_devices:
            if d.name == device_name:
                found = True
                d.kill_listen_stream()
                self.dce_devices.remove(d)
                print_to_ui(f"Device '{d.name}' removed.")

        for d in self.dte_devices:
            if d.name == device_name:
                found = True
                d.kill_listen_stream()
                self.dte_devices.remove(d)
                print_to_ui(f"Device '{d.name}' removed.")

        if not found:
            print_to_ui(f"Device {device_name} not found.")

    def print_threads(self):
        print_to_ui(self.listen_threads)

    def _listen_stream(self, device):
        """
        Listens for messages from the given device, then writes to all appropriate devices on bus.
        """
        print_to_ui(f"Listen stream started for {device.name}.")

        for message in device.listen():
            message = str(message)
            message_decoded = bytes.fromhex(message).decode('latin-1').rstrip().replace('\r', '')

            print_tape(device.sku, message_decoded)
            print_to_ui(f"Received {colored(device.type, device.type_color)} message from {device.name}:"
                                 f" {Fore.LIGHTWHITE_EX}{message_decoded}{Style.RESET_ALL}:"
                                 f" {message_decoded}")

            if device.mode == "DTE":
                # Messages from DTE devices get sent to all DCE devices.
                for d in self.dce_devices:
                    d.write(message)

            elif device.mode == "DCE":
                # Messages from DCE devices get sent to all DTE devices.
                for d in self.dte_devices:
                    d.write(message)

            else:
                print_to_ui("Mode not found")

        return True

    def _check_for_crashed_threads(self):
        """
        If a thread has thrown an error, attempt to restart it.
        """
        while True:
            for d in self.dce_devices:
                if d.exc and internet_connection():
                    # if the thread had an exception, start a new one
                    self._restart_thread(d)
            for d in self.dte_devices:
                if d.exc and internet_connection():
                    # if the thread had an exception, start a new one
                    self._restart_thread(d)
            time.sleep(.01)

    def _restart_thread(self, device):
        print_to_ui(f"Reconnecting to {device.name}.")
        device.kill_listen_stream()  # attempt to kill the listen thread if it is still responding
        device.exc = False  # reset the exception flag to false
        device.restart_session()  # start a new Session
        device.send_message_queue()  # send any messages saved in the queue
        if not device.mute:  # restart the listen thread if needed
            self.listen_threads[device.name] = threading.Thread(target=self._listen_stream, args=[device])
            self.listen_threads[device.name].daemon = True
            self.listen_threads[device.name].start()
        return
