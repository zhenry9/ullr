import datetime
import threading
import time

import requests
from urllib3.exceptions import ProtocolError

from dweet2ser import dweepy


class RemoteDevice(object):
    def __init__(self, thing_id, thing_key, from_dce_kw, from_dte_kw, mode, bucket, name="Unnamed Remote Device"):
        self.name = name
        self.thing_id = thing_id
        self.thing_key = thing_key
        self.mode = mode

        if mode == 'DTE':
            self.write_kw = from_dte_kw
            self.read_kw = from_dce_kw
        else:
            self.write_kw = from_dce_kw
            self.read_kw = from_dte_kw

        self._bucket = bucket
        self._session = requests.Session()
        self._last_message = ''
        self._kill_signal = "kill"

    def write(self, message):
        self._send_dweet({self.write_kw: message})

    def _send_dweet(self, content):
        try:
            dweepy.dweet_for(self.thing_id, content, key=self.thing_key, session=self._session)

        except dweepy.DweepyError as e:
            print(e)
            timestamp = str(datetime.datetime.now())
            print(timestamp + ":\tTrying again...")
            time.sleep(2)
            return self._send_dweet(content)

        except (ConnectionError, ProtocolError, OSError) as e:
            print(e.response)
            timestamp = str(datetime.datetime.now())
            print(timestamp + ":\tConnection closed by dweet, restarting (from send dweet):")
            self._bucket.put('crash', block=False)
            self._restart_session()
            return self._send_dweet(content)

    def _restart_session(self):
        self._session = requests.Session()

    def listen(self):
        keepalive_thread = threading.Thread(target=self._keepalive)
        keepalive_thread.daemon = True
        keepalive_thread.start()

        listen_thread = threading.Thread(target=self._listen_for_dweets)
        listen_thread.daemon = True
        listen_thread.start()

        # TODO: Fix ugly bad clunky way of catching crashes
        while True:
            if self._bucket.get() == 'crash':
                timestamp = str(datetime.datetime.now())
                print(timestamp + ":\tListen thread crashed, restarting.")
                # retrieve the last dweet and send to serial, in case it was missed during crash
                yield self.get_last_message()
                # kill any listen threads that are still alive and not crashed
                self._kill_listen_streams()
                time.sleep(.01)
                listen_thread = threading.Thread(target=self._listen_for_dweets)
                listen_thread.daemon = True
                listen_thread.start()

    def _listen_for_dweets(self):
        """ makes a call to dweepy to start a listening stream. error handling needs work
        """

        def catch_closed_connection():
            while True:
                try:
                    for dweet in dweepy.listen_for_dweets_from(self.thing_id, key=self.thing_key,
                                                               timeout=90000, session=self._session):
                        content = dweet["content"]
                        if self.read_kw in content:
                            if content[self.read_kw] == self._kill_signal:
                                return
                            yield content[self.read_kw]

                # if you get an error because dweet closed the connection, open it again.
                except (ConnectionError, ProtocolError, OSError) as e:
                    print(e.response)
                    timestamp = str(datetime.datetime.now())
                    print(timestamp + ":\tConnection closed by dweet, restarting:")
                    self._restart_session()
                    yield self.get_last_message()

                else:
                    timestamp = str(datetime.datetime.now())
                    print(timestamp + ":\tDweet listening thread died, restarting:")
                    self._restart_session()
                    yield self.get_last_message()

        return catch_closed_connection()

    def _kill_listen_streams(self):
        self._send_dweet({self.read_kw: self._kill_signal})

    def _keepalive(self):
        """ dweet.io seems to close the connection after 60 seconds of inactivity.
                    This sends a dummy payload every 45s to avoid that.
                """
        while True:
            time.sleep(45)
            self._send_dweet({"keepalive": 1})

    def get_last_message(self):
        return dweepy.get_latest_dweet_for(self.thing_id, key=self.thing_key, session=self._session)
