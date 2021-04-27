
import time
from queue import Queue
import threading

import serial
from serial.serialutil import SerialTimeoutException

from .utils import print_to_ui
from . import mqtt_client


class LocalDevice(object):
    """
    A device connected to a serial port on the local machine.
    """

    def __init__(self, port, mode, name="Local Device", mute=False, accepts_incoming=True, baudrate=9600, published=False, translation=[False, None, None, 0]):
        self.sku = id(self)
        self.name = name
        self.type = "serial"
        self.type_color = "red"
        self.port_name = port
        self.mode = mode
        self.accepts_incoming = accepts_incoming
        self.baudrate = baudrate
        self.published = published
        self.published_name = f"{mqtt_client.CLIENT_ID}/{self.name.replace(' ', '_')}"
        if self.published and self.accepts_incoming:
            mqtt_client.CLIENT.subscribe(self.published_name+"/from_remote")
            mqtt_client.CLIENT.message_callback_add(self.published_name+"/from_remote", self._remote_message)
        self.serial_port = serial.Serial(port=port,
                                         baudrate=baudrate,
                                         write_timeout=3)
        self.buffer = bytearray()
        self._last_message = ''
        self.mute = mute
        self.message_queue = Queue()
        self.translation = translation
        self.exc = False
        self.listening = False
        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def write(self, message: str):
        """
        Receives a hex string, converts to bytes and writes to the serial port.
        """
        if self.accepts_incoming:
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
            i = self.buffer.find(b"\r")
            while i >= 0:
                if len(self.buffer) > (i+1) and self.buffer[i+1:i+2] == b"\n":
                    i += 1
                message = self.buffer[:i+1]
                self.buffer = self.buffer[i+1:]
                self._last_message = message
                self.message_queue.put(message)
                if self.published:
                    mqtt_client.CLIENT.publish(self.published_name+"/from_device", message, qos=1)
                    print_to_ui("Published to MQTT.")
                i = self.buffer.find(b"\r")
            time.sleep(.1)
            i = max(1, min(2048, ser.in_waiting))
            data = ser.read(i)
            self.buffer.extend(data)

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

    def _remote_message(self, client, userdata, message):
        self.write(message.payload)
