
import uuid
import json
from datetime import datetime
from queue import Queue

from . import utils, mqtt_client
from .webapp.socketing import update_online_dot


class RemoteDevice(object):
    """
    Implementation of a serial device remotely connected to an MQTT broker
    """

    def __init__(self, topic_name, mode, mute=False, accepts_incoming=True, name="Remote Device", on_time_max=0,
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
            # cannot publish to device if no device name given
            self.accepts_incoming = False

        self.topic_name = f"{self.remote_client}/{self.remote_device_name}"
        self.mode = mode
        self.message_queue = Queue()
        self.late_message_queue = Queue()
        self._last_message = ''
        self.online = False
        self.listening = True
        self.remove_me = False
        self.translation = translation
        self.on_time_max = on_time_max
        mqtt_client.CLIENT.message_callback_add(self.topic_name+"/from_device", self._new_message)
        mqtt_client.add_subscription(self.topic_name+"/#")
        mqtt_client.subscribe_status(self.remote_client, self._update_status)

    def _update_status(self, status):
        if status == b"online":
            self.online = True
        else:
            self.online = False
        update_online_dot(self.sku, self.online)

    def _new_message(self, client, userdata, message):
        payload = json.loads(message.payload.decode())
        now_corrected = datetime.utcnow().timestamp() + mqtt_client.time_offset
        message_transit_time = now_corrected - payload["timestamp"]
        message_data = payload["message"]
        utils.logger.info(f"Message {message_data} transit time: {message_transit_time}.")
        if self.on_time_max == 0 or message_transit_time < self.on_time_max:
            self.message_queue.put(message_data.encode())
        else:
            self.late_message_queue.put(message_data.encode())

    def write(self, message):
        if self.accepts_incoming:
            mqtt_client.CLIENT.publish(self.topic_name+"/from_remote", message, qos=1)
            return True

    def kill_listen_stream(self):
        self.listening = False