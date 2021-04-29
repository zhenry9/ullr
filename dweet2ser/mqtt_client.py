import uuid

import paho.mqtt.client as mqtt

from .utils import logger, print_to_ui
from .webapp import socketing

MQTT_BROKER_URL, MQTT_BROKER_USER, MQTT_BROKER_PW = "", "", ""
MQTT_BROKER_PORT = 0
CLIENT_ID = hex(uuid.getnode())[2:].zfill(12)
CLIENT = None
CONNECTED = False

def on_connect(client, userdata, flags, rc):
    global CONNECTED
    if rc == 0:
        CONNECTED = True
        CLIENT.publish(CLIENT_ID+"/status", "online", qos=1, retain=True)
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

def start_client(url:str, port:int, username:str, pw:str):
    global CLIENT, MQTT_BROKER_PW, MQTT_BROKER_URL, MQTT_BROKER_USER, MQTT_BROKER_PORT
    MQTT_BROKER_URL = url
    MQTT_BROKER_PORT = port
    MQTT_BROKER_USER = username
    MQTT_BROKER_PW = pw
    CLIENT = mqtt.Client(CLIENT_ID, clean_session=False)
    CLIENT.on_connect = on_connect
    CLIENT.on_disconnect = on_disconnect
    CLIENT.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    CLIENT.username_pw_set(MQTT_BROKER_USER, MQTT_BROKER_PW)
    CLIENT.will_set(CLIENT_ID+"/status", "offline", qos=1, retain=True)
    CLIENT.reconnect_delay_set(min_delay=1, max_delay=8)
    CLIENT.connect_async(MQTT_BROKER_URL, MQTT_BROKER_PORT, keepalive=4)
    CLIENT.loop_start()
