import uuid

import paho.mqtt.client as mqtt
import ntplib

from .utils import logger, print_to_ui
from .webapp import socketing

MQTT_BROKER_URL, MQTT_BROKER_USER, MQTT_BROKER_PW = "", "", ""
MQTT_BROKER_PORT = 0
CLIENT_ID = hex(uuid.getnode())[2:].zfill(12)
CLIENT = None
CONNECTED = False
time_offset = 0

status_functions = {}
subscriptions = []
ntp_client = ntplib.NTPClient()

def update_time_offset():
    global time_offset
    try:
        resp = ntp_client.request('pool.ntp.org')
        time_offset = resp.offset
        logger.info(f"Time offset set to {time_offset}.")
        return True
    except:
        logger.warn("Unable to update time offset.")
        return False

def on_connect(client, userdata, flags, rc):
    global CONNECTED
    update_time_offset()
    if rc == 0:
        CONNECTED = True
        CLIENT.publish(CLIENT_ID+"/status", "online", qos=1, retain=True)
        for topic in subscriptions:
            CLIENT.subscribe(topic, qos=1)
        print_to_ui("Connected to MQTT broker.")
        socketing.update_client_status(True)
    else:
        print_to_ui(f"Connection to MQTT broker failed: code {rc}")
        socketing.update_client_status(False)

def on_disconnect(client, userdata, rc):
    global CONNECTED
    CONNECTED = False
    print_to_ui("Disconnected from MQTT broker.")
    socketing.update_client_status(False)

def on_message(client, userdata, message):
    split_topic = message.topic.split("/")
    if len(split_topic) > 1 and split_topic[1] == "status":
        for client_name in status_functions.keys():
            if split_topic[0] == client_name:
                for func in status_functions[client_name]:
                    func(message.payload)

def add_subscription(topic):
    global subscriptions
    subscriptions.append(topic)
    CLIENT.subscribe(topic, qos=1)

def subscribe_status(host_name, cb_function):
    global status_functions
    if status_functions.get(host_name) is None:
        status_functions[host_name] = []
    status_functions[host_name].append(cb_function)
    add_subscription(host_name+"/status")

def start_client(url:str, port:int, username:str, pw:str):
    global CLIENT, MQTT_BROKER_PW, MQTT_BROKER_URL, MQTT_BROKER_USER, MQTT_BROKER_PORT
    MQTT_BROKER_URL = url
    MQTT_BROKER_PORT = port
    MQTT_BROKER_USER = username
    MQTT_BROKER_PW = pw
    CLIENT = mqtt.Client(CLIENT_ID, clean_session=False)
    CLIENT.on_connect = on_connect
    CLIENT.on_disconnect = on_disconnect
    CLIENT.on_message = on_message
    CLIENT.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    CLIENT.username_pw_set(MQTT_BROKER_USER, MQTT_BROKER_PW)
    CLIENT.will_set(CLIENT_ID+"/status", "offline", qos=1, retain=True)
    CLIENT.reconnect_delay_set(min_delay=1, max_delay=8)
    CLIENT.connect_async(MQTT_BROKER_URL, MQTT_BROKER_PORT, keepalive=4)
    CLIENT.loop_start()
