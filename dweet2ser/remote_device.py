import datetime
import threading
import time

import requests
from termcolor import colored
from urllib3.exceptions import ProtocolError

from dweet2ser import dweepy
from dweet2ser.settings import timestamp, internet_connection, s_print


class DeadConnectionError(Exception):
    pass


class RemoteDevice(object):
    """
    Implementation of a serial device remotely connected with dweet.io
    """
    def __init__(self, thing_id, mode, thing_key=None, name="Remote Device", mute=False):
        self.name = name
        self.type = "dweet"
        self.type_color = "cyan"
        self.thing_id = thing_id
        self.locked = False
        self.thing_key = thing_key
        self.mute = mute
        if thing_key is not None:
            self.locked = True
        self.mode = mode

        if mode == 'DCE':  # if this is a DCE (device), set the dweet.io keywords appropriately
            self.write_kw = "from_pc"
            self.read_kw = "from_device"
        else:  # if this is a DTE (computer), the dweet.io keywords should be reversed.
            self.write_kw = "from_device"
            self.read_kw = "from_pc"

        self._session = requests.Session()
        self._last_message = ''
        self._kill_signal = "kill"
        self._message_queue = []
        self._started_on_day = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        self.exc = False
        self.listening = False

    def write(self, message):
        """
        Tries to send a dweet message to the remote device. If there's no internet connection it saves
        the message to a queue.
        """
        if internet_connection():
            # check for a connection before trying to send to dweet
            self._send_dweet({self.write_kw: message})
            message_decoded = bytes.fromhex(message).decode('latin-1').rstrip()
            s_print(f"{timestamp()}{colored(self.type.capitalize(), self.type_color)} sent to {self.name}: "
                    f"{message_decoded}")
        else:
            # if there's no connection save the message to resend on reconnect
            s_print(f"{timestamp()}No connection to {self.name}. Saving message to queue.")
            self._message_queue.append(message)
            self.exc = True

    def send_message_queue(self):
        """
        Attempt to send queued messages.
        """
        while len(self._message_queue) > 0 and internet_connection():
            s_print(f"{timestamp()}Sending queued messages.")
            self.write(self._message_queue.pop(0))
            time.sleep(1.2)  # avoid exceeding dweet.io's 1s rate limit

    def _send_dweet(self, content):
        try:
            dweepy.dweet_for(self.thing_id, content, key=self.thing_key, session=self._session)

        except dweepy.DweepyError as e:
            s_print(timestamp() + str(e))
            s_print(f"{timestamp()}Trying again...")
            time.sleep(1.5)
            return self._send_dweet(content)

        except (ConnectionError, ProtocolError, OSError) as e:
            s_print(timestamp() + str(e))
            s_print(f"{timestamp()}Connection to {self.name} lost.")
            self.exc = True
            return

    def restart_session(self):
        """
        Gets a new Session from requests.
        """
        self._session = requests.Session()

    def listen(self):
        """
        Calls the listen/for/dweets/from function of dweet.io and yields messages from the chunked
        HTTP response.
        """
        self.listening = True
        # Start a thread to send a message to dweet every 45 seconds.
        # This is necessary because dweet.io closes the listen response after 60s of inactivity.
        keepalive_thread = threading.Thread(target=self._keepalive)
        keepalive_thread.daemon = True
        keepalive_thread.start()

        for message in self._listen_for_dweets():
            yield message

    def _listen_for_dweets(self):
        """ makes a call to dweepy to start a listening stream. error handling needs work
        """
        while internet_connection() and self.listening:
            try:
                for dweet in dweepy.listen_for_dweets_from(self.thing_id, key=self.thing_key,
                                                           timeout=90000, session=self._session):
                    content = dweet["content"]
                    self._last_message = dweet
                    if self.read_kw in content:
                        message = content[self.read_kw]
                        if message == self._kill_signal:
                            s_print(f"{timestamp()}Listen stream for {self.name} closed.")
                            return
                        yield message

            # if you get an error because dweet closed the connection, open it again.
            except (ConnectionError, ProtocolError, OSError) as e:
                s_print(timestamp() + str(e))
                s_print(f"{timestamp()}Connection closed by dweet, restarting.")
                self.restart_session()
                yield self.get_last_message()
        s_print(f"{timestamp()}Listen stream for {self.name} closed.")
        self.exc = True
        return

    def kill_listen_stream(self):
        """
        Attempts to manually end the chunked HTTP listening stream.
        """
        self._send_dweet({self.read_kw: self._kill_signal})
        self.listening = False

    def _keepalive(self):
        """ dweet.io seems to close the connection after 60 seconds of inactivity.
            This sends a dummy payload every 45s to avoid that.
        """
        while self.listening and not self.exc:
            time.sleep(45)
            self._send_dweet({"keepalive": 1})

    def get_last_message(self):
        """
        Tries to recover the last message sent to dweet.
        """
        message = ''
        if internet_connection():
            dweet = dweepy.get_latest_dweet_for(self.thing_id, key=self.thing_key, session=self._session)
            content = dweet[0]["content"]
            if self.read_kw in content:
                message = content[self.read_kw]
        return message

    @staticmethod
    def _get_dweet_time(dweet):
        """
        For future dweet recovery implementation.
        """
        created = dweet["created"].replace("T", " ").replace("Z", "")
        dweet_time = datetime.datetime.fromisoformat(created)
        return dweet_time

# TODO Create function to retrieve dweets from storage after a connection loss.
#   Basic idea: store time of last_message_received from listen.
#   On connection restore, pull all dweets from today and yield all where "created" > last_message_received
