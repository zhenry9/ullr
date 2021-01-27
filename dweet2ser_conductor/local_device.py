
import time

import serial
from termcolor import colored

from settings import timestamp


class LocalDevice(object):

    def __init__(self, port, mode, name="Unnamed Local Device"):
        self.name = name
        self.type = "serial"
        self.type_color = "red"
        self.port_name = port
        self.mode = mode
        self.serial_port = serial.Serial(self.port_name)
        self._last_message = ''
        self.mute = False
        self.exc = False

    def write(self, message):
        if type(message) is not str:  # make sure the message is a string
            message = str(message)
        message_bytes = bytes.fromhex(message)  # convert dweet string into bytes for RS232.
        message_decoded = message_bytes.decode('latin-1').rstrip()
        print(f"{timestamp()}{colored(self.type.capitalize(), self.type_color)} message to {self.name}: {message_decoded}")
        return self.serial_port.write(message_bytes)

    def listen(self):
        """listens to serial port, yields what it hears
        """
        ser = self.serial_port

        # TODO: test with a variety of devices and protocols
        while not self.mute:
            if ser.in_waiting > 0:
                ser_data = ser.read(ser.in_waiting)
                self._last_message = ser_data.hex()
                yield ser_data.hex()
            else:
                time.sleep(0.0001)

    def kill_listen_stream(self):
        self.mute = True

    def get_last_message(self):
        return self._last_message
