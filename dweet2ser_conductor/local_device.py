
import threading
from queue import Queue

import serial


class LocalDevice(object):

    def __init__(self, port, mode, name="Unnamed Local Device"):
        self.name = name
        self.type = "serial"
        self.type_color = "red"
        self.port_name = port
        self.mode = mode
        self.serial_port = serial.Serial(self.port_name)
        self._buffer = Queue()
        self._last_message = ''
        self.mute = False
        self.exc = False

    def write(self, message):
        if type(message) is not str:  # make sure the message is a string
            message = str(message)
        message_bytes = bytes.fromhex(message)  # convert dweet string into bytes for RS232.
        return self.serial_port.write(message_bytes)

    def listen(self):
        """listens to serial port, yields what it hears
        """
        ser = self.serial_port
        # TODO: find a way to listen to serial without an infinite loop
        # TODO: verify readline() will work with data other than CP540
        while True:
            if ser.in_waiting > 0:
                ser_data = ser.readline()
                self._last_message = ser_data.hex()
                yield ser_data.hex()

    def get_last_message(self):
        return self._last_message
