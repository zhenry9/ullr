import threading
import time

from termcolor import colored
from colorama import init as colorama_init, Fore, Style

from settings import timestamp, internet_connection

colorama_init()


def _print_device_list(dev_list):
    cols = ["#".ljust(3),
            "Name".ljust(16),
            "Type".ljust(10),
            "Port".ljust(15),
            "ThingName".ljust(20),
            "Locked".ljust(6),
            ]
    header = ''
    for col in cols:
        header = header + f"{col}  "
    print(f"\t{Fore.LIGHTWHITE_EX}{header}{Style.RESET_ALL}")

    for i in range(0, len(dev_list)):
        num = str(i + 1)
        d = dev_list[i]
        if type(d).__name__ == "LocalDevice":
            print(f"\t"
                  f"{num.ljust(3)}  "
                  f"{d.name.ljust(16)}  "
                  f"{colored(d.type.ljust(10), d.type_color)}  "
                  f"{d.port_name.ljust(15)}")
        if type(d).__name__ == "RemoteDevice":
            print(f"\t"
                  f"{num.ljust(3)}  "
                  f"{d.name.ljust(16)}  "
                  f"{colored(d.type.ljust(10), d.type_color)}  "
                  f"{''.ljust(15)}  "
                  f"{d.thing_id.ljust(20)}  "
                  f"{str(d.locked).ljust(6)}  "
                  )


class DeviceBus(object):
    def __init__(self):
        self.dce_devices = []
        self.dte_devices = []
        self.listen_threads = {}

        self.stream_restarter = threading.Thread(target=self._check_for_crashed_threads)
        self.stream_restarter.daemon = True
        self.stream_restarter.start()

    def add_device(self, device):
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
        found = False
        for d in self.dce_devices:
            if d.name == device_name:
                found = True
                d.kill_listen_stream()
                self.dce_devices.remove(d)
                print(f"{timestamp()}Device '{d.name}' removed.")

        for d in self.dte_devices:
            if d.name == device_name:
                found = True
                d.kill_listen_stream()
                self.dte_devices.remove(d)
                print(f"{timestamp()}Device '{d.name}' removed.")

        if not found:
            print("Device not found.")

    def print_status(self):
        print("\nDCE Devices")
        _print_device_list(self.dce_devices)
        print("\nDTE Devices")
        _print_device_list(self.dte_devices)

    def print_threads(self):
        print(self.listen_threads)

    def _listen_stream(self, device):
        print(f"\n{timestamp()}Listen stream started for {device.name}.")

        for message in device.listen():
            message = str(message)
            message_decoded = bytes.fromhex(message).decode('latin-1').rstrip()

            print(f"\n{timestamp()}Received {colored(device.type, device.type_color)} message from {device.name}:"
                  f" {Fore.LIGHTWHITE_EX}{message_decoded}{Style.RESET_ALL}")

            if device.mode == "DTE":
                for d in self.dce_devices:
                    d.write(message)

            elif device.mode == "DCE":
                for d in self.dte_devices:
                    d.write(message)

            else:
                print("Mode not found")

        return True

    def _check_for_crashed_threads(self):
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
        print(f"{timestamp()}Reconnecting to {device.name}.")
        device.exc = False
        device.restart_session()
        device.send_message_queue()
        if not device.mute:
            self.listen_threads[device.name] = threading.Thread(target=self._listen_stream, args=[device])
            self.listen_threads[device.name].daemon = True
            self.listen_threads[device.name].start()
        return
