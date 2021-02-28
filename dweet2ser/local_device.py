
import time

import serial

from .utils import print_to_ui

class LocalDevice(object):
    """
    A device connected to a serial port on the local machine.
    """
    def __init__(self, port, mode, name="Local Device", mute=False, baudrate=9600):
        self.sku = id(self)
        self.name = name
        self.type = "serial"
        self.type_color = "red"
        self.port_name = port
        self.mode = mode
        self.baudrate = baudrate
        self.serial_port = serial.Serial(port=port,
                                         baudrate=baudrate,
                                         timeout=0.1)
        self._last_message = ''
        self.mute = mute
        self.exc = False
        self.listening = False

    def write(self, message: str):
        """
        Receives a hex string, converts to bytes and writes to the serial port.
        """
        if type(message) is not str:  # make sure the message is a string
            message = str(message)
        message_bytes = bytes.fromhex(message)  # convert dweet string into bytes for RS232.
        message_decoded = message_bytes.decode('latin-1').rstrip()
        print_to_ui(f"{self.type.capitalize()} message sent to {self.name}: {message_decoded}")
        return self.serial_port.write(message_bytes)

    def listen(self):
        """listens to serial port, yields what it hears
        """
        ser = self.serial_port
        self.listening = True

        # TODO: test with a variety of devices and protocols
        while self.listening:
            if ser.in_waiting > 0:
                ser_data = ser.read(100)
                self._last_message = ser_data.hex()
                yield ser_data.hex()
            else:
                time.sleep(0.0001)

    def kill_listen_stream(self):
        """
        Stops any threads listening to the serial port.
        """
        self.listening = False

    def get_last_message(self):
        """
        Returns the last message read from the serial port.
        """
        return self._last_message
