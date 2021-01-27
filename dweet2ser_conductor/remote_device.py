import threading
import time

import requests
from termcolor import colored
from urllib3.exceptions import ProtocolError

from dweet2ser_conductor import dweepy
from settings import timestamp, internet_connection


class DeadConnectionError(Exception):
    pass


class RemoteDevice(object):
    def __init__(self, thing_id, thing_key, mode, name="Unnamed Remote Device"):
        self.name = name
        self.type = "dweet"
        self.type_color = "cyan"
        self.thing_id = thing_id
        self.locked = False
        self.thing_key = thing_key
        self.mute = False
        if thing_key is not None:
            self.locked = True
        self.mode = mode

        if mode == 'DCE':
            self.write_kw = "from_pc"
            self.read_kw = "from_device"
        else:
            self.write_kw = "from_device"
            self.read_kw = "from_pc"

        self._session = requests.Session()
        self._last_message = ''
        self._kill_signal = "kill"
        self._message_queue = []
        self.exc = False

    def write(self, message):
        if internet_connection():
            # check for a connection before trying to send to dweet
            self._send_dweet({self.write_kw: message})
            message_decoded = bytes.fromhex(message).decode('latin-1').rstrip()
            print(f"{timestamp()}{colored(self.type.capitalize(), self.type_color)} sent to {self.name}: {message_decoded}")
        else:
            # if there's no connection save the message to resend on reconnect
            print(f"{timestamp()}No connection to {self.name}. Saving message to queue.")
            self._message_queue.append(message)
            self.exc = True

    def send_message_queue(self):
        while len(self._message_queue) > 0:
            print(f"{timestamp()}Sending queued messages.")
            self.write(self._message_queue.pop(0))
            time.sleep(1.2)  # avoid exceeding dweet.io's 1s rate limit

    def _send_dweet(self, content):
        try:
            dweepy.dweet_for(self.thing_id, content, key=self.thing_key, session=self._session)

        except dweepy.DweepyError as e:
            print(timestamp() + str(e))
            print(f"{timestamp()}Trying again...")
            time.sleep(1.5)
            return self._send_dweet(content)

        except (ConnectionError, ProtocolError, OSError) as e:
            print(timestamp() + str(e))
            print(f"{timestamp()}Connection to {self.name} lost.")
            self.exc = True
            return

    def restart_session(self):
        self._session = requests.Session()

    def listen(self):
        keepalive_thread = threading.Thread(target=self._keepalive)
        keepalive_thread.daemon = True
        keepalive_thread.start()

        for message in self._listen_for_dweets():
            yield message

    def _listen_for_dweets(self):
        """ makes a call to dweepy to start a listening stream. error handling needs work
        """
        while internet_connection():
            try:
                for dweet in dweepy.listen_for_dweets_from(self.thing_id, key=self.thing_key,
                                                           timeout=90000, session=self._session):
                    content = dweet["content"]
                    if self.read_kw in content:
                        message = content[self.read_kw]
                        if message == self._kill_signal:
                            print(f"{timestamp()}Listen stream for {self.name} closed.")
                            return
                        yield message

            # if you get an error because dweet closed the connection, open it again.
            except (ConnectionError, ProtocolError, OSError) as e:
                print(timestamp() + str(e))
                print(f"{timestamp()}Connection closed by dweet, restarting.")
                self.restart_session()
                yield self.get_last_message()
        print(f"{timestamp()}Listen stream for {self.name} closed.")
        self.exc = True
        return

    def kill_listen_stream(self):
        self._send_dweet({self.read_kw: self._kill_signal})

    def _keepalive(self):
        """ dweet.io seems to close the connection after 60 seconds of inactivity.
                    This sends a dummy payload every 45s to avoid that.
                """
        while not self.exc:
            time.sleep(45)
            self._send_dweet({"keepalive": 1})

    def get_last_message(self):
        message = ''
        if internet_connection():
            dweet = dweepy.get_latest_dweet_for(self.thing_id, key=self.thing_key, session=self._session)
            content = dweet[0]["content"]
            if self.read_kw in content:
                message = content[self.read_kw]
        return message

# TODO Create function to retrieve dweets from storage after a connection loss.
#   Basic idea: store time of last_message_received from listen.
#   On connection restore, pull all dweets from today and yield all where "created" > last_message_received
