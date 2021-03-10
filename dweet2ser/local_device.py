
import time

import serial
from serial.serialutil import SerialTimeoutException

from .utils import print_to_ui


class LocalDevice(object):
    """
    A device connected to a serial port on the local machine.
    """

    def __init__(self, port, mode, name="Local Device", mute=False, baudrate=9600, translation=[False, None, None, 0]):
        self.sku = id(self)
        self.name = name
        self.type = "serial"
        self.type_color = "red"
        self.port_name = port
        self.mode = mode
        self.baudrate = baudrate
        self.serial_port = serial.Serial(port=port,
                                         baudrate=baudrate,
                                         timeout=round(1/(baudrate/500), 1),
                                         write_timeout=3)
        self._last_message = ''
        self.mute = mute
        self.translation = translation
        self.exc = False
        self.listening = False

    def write(self, message: str):
        """
        Receives a hex string, converts to bytes and writes to the serial port.
        """
        if type(message) is not str:  # make sure the message is a string
            message = str(message)
        # convert dweet string into bytes for RS232.
        message_bytes = bytes.fromhex(message)
        try:
            self.serial_port.write(message_bytes)
            return True
        except SerialTimeoutException:
            return False

    def listen(self):
        """listens to serial port, yields what it hears
        """
        ser = self.serial_port
        self.listening = True

        while self.listening:
            if ser.in_waiting > 0:
                ser_data = ser.read(100)
                self._last_message = ser_data.hex()
                yield ser_data.hex()
            else:
                time.sleep(0.0001)
        self.serial_port.close()

        return

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
