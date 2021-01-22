import threading
from datetime import datetime


class DeviceBus(object):
    def __init__(self):
        self.dce_devices = []
        self.dte_devices = []
        self.listen_threads = {}

    def add_dte(self, device):
        self.dte_devices.append(device)
        if not device.mute:
            self.listen_threads[device.name] = threading.Thread(target=self._listen_stream, args=[device])
        return True

    def add_dce(self, device):
        self.dce_devices.append(device)
        if not device.mute:
            self.listen_threads[device.name] = threading.Thread(target=self._listen_stream, args=[device])
        return True

    def _listen_stream(self, device):
        for message in device.listen():
            timestamp = datetime.now()
            print(f"\n{timestamp}: Received message from {device.name}:\t{message}")
            if device.mode == "DTE":
                for d in self.dce_devices:
                    d.write(message)
                    print(f"{timestamp}: Written to {d.name}")
            elif device.mode == "DCE":
                for d in self.dte_devices:
                    d.write(message)
                    print(f"{timestamp}: Written to {d.name}")
        return True
