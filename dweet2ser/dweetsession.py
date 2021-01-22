# standard imports
import datetime
import queue
import threading
import time
from configparser import ConfigParser

# 3rd party imports
from dweet2ser import dweepy
import requests
import serial
from colorama import init
from termcolor import colored
from urllib3.exceptions import ProtocolError

# colorama call
init()


class DweetSession(object):

    def __init__(self, thing_id, key, pc_keyword, device_keyword, port, mode, bucket):
        self.thingId = thing_id
        self.key = key
        self.port = port
        self.mode = mode
        self.session = requests.Session()
        self.serial_port = serial.Serial(port)
        self.bucket = bucket
        self.kill_signal = "kill"

        # in DTE (pc) mode look for dweets under the device keyword, write dweets under the PC keyword
        if mode == 'DTE':
            self.fromThisDevice = pc_keyword
            self.fromThatDevice = device_keyword

        # in DCE (device) mode look for dweets under the PC keyword, write dweets under the device keyword
        elif mode == 'DCE':
            self.fromThisDevice = device_keyword
            self.fromThatDevice = pc_keyword

    @classmethod
    def from_config_file(cls, config_file, port, mode, bucket):
        # open our config file
        cfg = ConfigParser()
        cfg.read(config_file)

        return cls.from_config_parser(cfg, port, mode, bucket)

    @classmethod
    def from_config_parser(cls, cfg, port, mode, bucket):

        # get thing ID from config file
        thing_id = cfg.get("User", "thing_id")
        thing_key = cfg.get("User", "key")
        if thing_key == 'None' or thing_key == '':
            thing_key = None

        # get some defaults out of the config file
        default_pc_keyword = cfg.get("User", "pc_keyword")
        default_device_buffer = cfg.get("User", "device_keyword")

        if port is None:
            if mode == 'DTE':
                port = cfg.get("User", "DTE_port")
            if mode == 'DCE':
                port = cfg.get("User", "DCE_port")

        return cls(thing_id, thing_key, default_pc_keyword, default_device_buffer, port, mode, bucket)

    def start(self):
        threads = [threading.Thread(target=self._listen_to_serial),
                   threading.Thread(target=self._listen_to_dweet)]

        if self.mode == "DTE":
            threads.append(threading.Thread(target=self._keepalive))

        for thread in threads:
            thread.daemon = True

        for thread in threads:
            thread.start()

    def restart_session(self):
        """ starts a new requests session
        """
        self.session = requests.Session()

    def _kill_listen_streams(self):
        self.send_dweet({self.fromThatDevice: "kill"})

    def send_dweet(self, content):
        try:
            dweepy.dweet_for(self.thingId, content, key=self.key, session=self.session)

        except dweepy.DweepyError as e:
            print(e)
            timestamp = str(datetime.datetime.now())
            print(timestamp + ":\tTrying again...")
            time.sleep(2)
            return self.send_dweet(content)

        except (ConnectionError, ProtocolError, OSError) as e:
            print(e.response)
            timestamp = str(datetime.datetime.now())
            print(timestamp + ":\tConnection closed by dweet, restarting (from send dweet):")
            self.bucket.put('crash', block=False)
            self.restart_session()
            return self.send_dweet(content)

    def get_latest_dweet(self):
        return dweepy.get_latest_dweet_for(self.thingId, key=self.key, session=self.session)

    def print_info(self):
        print(f"\tThing name: {self.thingId}\n"
              f"\tKey used: {self.key is not None}\n"
              f"\tReading from keyword: {self.fromThatDevice}\n"
              f"\tWriting to keyword: {self.fromThisDevice}\n"
              f"\tUsing serial port: {self.port}"
              )

    def _dweet_stream(self):
        """ makes a call to dweepy to start a listening stream. error handling needs work
        """

        def catch_closed_connection():
            while True:
                try:
                    for dweet in dweepy.listen_for_dweets_from(self.thingId, key=self.key,
                                                               timeout=90000, session=self.session):
                        yield dweet

                # if you get an error because dweet closed the connection, open it again.
                except (ConnectionError, ProtocolError, OSError) as e:
                    print(e.response)
                    timestamp = str(datetime.datetime.now())
                    print(timestamp + ":\tConnection closed by dweet, restarting (from listen):")
                    self.restart_session()
                    yield self.get_latest_dweet()

                else:
                    timestamp = str(datetime.datetime.now())
                    print(timestamp + ":\tDweet listening thread died, restarting:")
                    self.restart_session()
                    yield self.get_latest_dweet()

        return catch_closed_connection()

    def _listen(self):
        target = self.fromThatDevice
        for dweet in self._dweet_stream():
            content = dweet["content"]
            if target in content:
                if content[target] == self.kill_signal:
                    return
                self._write_to_serial(content[target])

    def _write_to_serial(self, output):
        if type(output) is not str:  # make sure the output is a string
            output = str(output)
        output_bytes = bytes.fromhex(output)  # convert dweet string into bytes for RS232.
        self.serial_port.write(output_bytes)
        timestamp = str(datetime.datetime.now())
        output_text = output_bytes.strip().decode('latin-1')
        print(timestamp + ":\treceived " + colored("dweet", "cyan"))
        print("\t\t\t\t" + output_text)
        print("\t\t\t\twritten to " + colored("serial\n", "red"))

    def write_last_dweet_to_serial(self):
        target = self.fromThatDevice
        dweet = self.get_latest_dweet()
        content = dweet[0]["content"]
        if target in content:
            self._write_to_serial(content[target])

    def _listen_to_dweet(self):
        """
        Starts listening for dweets. Watches the bucket and restarts the thread if a crash message is received.
        """
        # TODO: this seems pretty ugly. Figure out why stream crashes silently and find a better fix

        t = threading.Thread(target=self._listen)
        t.daemon = True
        t.start()
        while True:
            try:
                # if another thread wrote a crash message it's time to restart the stream
                if self.bucket.get(block=False) == 'crash':
                    timestamp = str(datetime.datetime.now())
                    print(timestamp + ":\tListen thread crashed, restarting.")
                    # retrieve the last dweet and send to serial, in case it was missed during crash
                    self.write_last_dweet_to_serial()
                    # kill any listen threads that are still alive and not crashed
                    self._kill_listen_streams()
                    time.sleep(.01)
                    t = threading.Thread(target=self._listen)
                    t.daemon = True
                    t.start()
            except queue.Empty:
                time.sleep(.01)
                pass

    def _listen_to_serial(self):
        """listens to serial port, if it hears something it dweets it
        """
        ser = self.serial_port
        target = self.fromThisDevice
        # TODO: find a way to listen to serial without an infinite loop
        # TODO: verify readline() will work with data other than CP540
        while True:
            if ser.in_waiting > 0:
                ser_data = ser.readline()
                timestamp = str(datetime.datetime.now())
                print(timestamp + ":\treceived " + colored("serial data", "red"))
                print("\t\t\t\t " + ser_data.strip().decode('latin-1'))
                print("\t\t\t\tsent to  " + colored("dweet.io\n", "cyan"))
                self.send_dweet({target: ser_data.hex()})

    def _keepalive(self):
        """ dweet.io seems to close the connection after 60 seconds of inactivity.
            This sends a dummy payload every 45s to avoid that.
        """
        while True:
            time.sleep(45)
            self.send_dweet({"keepalive": 1})
