
import uuid
from queue import Queue

from . import utils, mqtt_client
from .webapp.socketing import update_online_dot


class RemoteDevice(object):
    """
    Implementation of a serial device remotely connected to an MQTT broker
    """

    def __init__(self, topic_name, mode, mute=False, accepts_incoming=True, name="Remote Device",
                 translation=[False, None, None, 0]):
        self.sku = id(self)
        self.name = name
        self.mute = mute
        self.accepts_incoming = accepts_incoming
        self.type = "mqtt"
        self.type_color = "cyan"
        parsed_topic = topic_name.split("/")
        self.remote_client = parsed_topic[0]

        # if a device name was not given, subscribe to all devices on remote
        if len(parsed_topic) > 1:
            self.remote_device_name = parsed_topic[1]
        else:
            self.remote_device_name = "+"

        self.topic_name = f"{self.remote_client}/{self.remote_device_name}"
        self.mode = mode
        self.message_queue = Queue()
        self._last_message = ''
        self.online = False
        self.listening = True
        self.remove_me = False
        self.translation = translation
        mqtt_client.CLIENT.message_callback_add(self.remote_client+"/status", self._update_status)
        mqtt_client.CLIENT.message_callback_add(self.topic_name+"/from_device", self._new_message)
        mqtt_client.CLIENT.subscribe(self.remote_client+"/status")
        mqtt_client.CLIENT.subscribe(self.topic_name+"/#", qos=1)

    def _update_status(self, client, userdata, message):
        if message.payload == b"online":
            self.online = True
        else:
            self.online = False
        update_online_dot(self.sku, self.online)

    def _new_message(self, client, userdata, message):
        self.message_queue.put(message.payload)

    def write(self, message):
        if self.accepts_incoming:
            mqtt_client.CLIENT.publish(self.topic_name+"/from_remote", message, qos=1)
            return True

    def kill_listen_stream(self):
        self.listening = False