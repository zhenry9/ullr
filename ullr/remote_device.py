
import uuid
import json
import time
from queue import Queue

from . import utils, mqtt_client
from .webapp.socketing import update_online_dot, update_late_badge


class RemoteDevice(object):
    """
    Implementation of a serial device remotely connected to an MQTT broker
    """

    def __init__(self, topic_name, mode, mute=False, accepts_incoming=True, name="Remote Device", on_time_max=0,
                 translation=[False, None, None, 0]):
        self.sku = id(self)
        if name[0] == "$":
            raise ValueError("Device name cannot start with '$'.")
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
        self.late_message_list= []
        self._last_message = ''
        self.online = False
        self.listening = True
        self.remove_me = False
        self.translation = translation
        self.on_time_max = int(on_time_max)
        mqtt_client.client.message_callback_add(self.topic_name+"/from_device", self._new_message)
        mqtt_client.add_subscription(self.topic_name+"/#")
        mqtt_client.subscribe_status(self.remote_client, self._update_status)
        self.max_transit_time = 0
        self.min_transit_time = 9999
        self.average_transit_time = 0
        self.received_messages_count = 0

    def _update_status(self, status):
        if status == b"online":
            self.online = True
        else:
            self.online = False
        update_online_dot(self.sku, self.online)
    
    def _update_transit_stats(self, transit_time):
        self.min_transit_time = min(self.min_transit_time, transit_time)
        self.max_transit_time = max(self.max_transit_time, transit_time)
        sum_recalc = self.average_transit_time * self.received_messages_count
        self.received_messages_count += 1
        self.average_transit_time = round((sum_recalc + transit_time)/self.received_messages_count, 2)

    def _new_message(self, client, userdata, message):
        if self.listening:
            try:
                payload = json.loads(message.payload.decode())
                now_corrected = time.time() + mqtt_client.time_offset
                message_transit_time = round(now_corrected - payload["timestamp"], 1)
                self._update_transit_stats(message_transit_time)
                message_data = payload["message"]
                stripped_message = " ".join(message_data.split())
                utils.logger.info(f"Message {stripped_message} transit time: {message_transit_time}.")
                if self.on_time_max == 0 or message_transit_time < self.on_time_max:
                    self.message_queue.put(message_data.encode())
                else:
                    self.late_message_list.append(message_data.encode())
                    utils.print_to_ui(f"Received message from {self.name} "
                                    f"after max on-time window of {self.on_time_max}s ({message_transit_time}s). "
                                    f"Adding to late message list.")
                    update_late_badge(self.sku, len(self.late_message_list))
            except Exception as e:
                utils.print_to_ui(f"Error receiving remote message: {e}")

    def write(self, message):
        if self.accepts_incoming and self.remote_device_name != "+":
            mqtt_client.client.publish(self.topic_name+"/from_remote", message, qos=1)
            return True
        return False

    def accept_late_messages(self, message_index_list=None):
        if message_index_list is not None:
            temp_list = []
            message_index_list.sort(reverse=True)
            for index in message_index_list:
                temp_list.append(self.late_message_list.pop(index))
            while len(temp_list) > 0:
                self.message_queue.put(temp_list.pop())
        else:
            for message in self.late_message_list:
                self.message_queue.put(message)
                self.late_message_list.remove(message)
        update_late_badge(self.sku, len(self.late_message_list))

    def kill_listen_stream(self):
        self.listening = False