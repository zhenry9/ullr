
from threading import Lock, Thread
import time

import paho.mqtt.client as mqtt
import ntplib
import certifi

from .utils import logger, print_to_ui, internet_connection
from .webapp import socketing

mqtt_broker_url, mqtt_broker_user, mqtt_broker_pw, CLIENT_ID = "", "", "", ""
mqtt_broker_port = 0

client = None

connected = False
time_offset = 0

status_functions = {}
subscriptions = []
ntp_client = ntplib.NTPClient()
publish_lock = Lock()


def update_time_offset():
    while not internet_connection():
        time.sleep(2)
    global time_offset
    try:
        resp = ntp_client.request('pool.ntp.org')
        time_offset = resp.offset
        logger.info(f"Time offset set to {time_offset}.")
        return True
    except:
        logger.warn("Unable to update time offset.")
        return update_time_offset()


def safe_publish(*args, **kwargs):
    with publish_lock:
        client.publish(*args, **kwargs)


def on_connect(client, userdata, flags, rc):
    global connected

    t = Thread(target=update_time_offset)
    t.daemon = True
    # t.start()  # removed due to inaccuracies running on raspberry pi at boot
    if rc == 0:
        connected = True
        safe_publish(CLIENT_ID+"/status", "online", qos=1, retain=True)
        for topic in subscriptions:
            client.subscribe(topic, qos=1)
        print_to_ui("Connected to MQTT broker.")
        socketing.update_client_status(True)
    else:
        print_to_ui(f"Connection to MQTT broker failed: code {rc}")
        socketing.update_client_status(False)


def on_disconnect(client, userdata, rc):
    global connected
    connected = False
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
    client.subscribe(topic, qos=1)


def subscribe_status(host_name, cb_function):
    global status_functions
    if status_functions.get(host_name) is None:
        status_functions[host_name] = []
    status_functions[host_name].append(cb_function)
    add_subscription(host_name+"/status")


def start_client(url: str, port: int, username: str, pw: str, client_id=CLIENT_ID):
    global CLIENT_ID, client, mqtt_broker_pw, mqtt_broker_url, mqtt_broker_user, mqtt_broker_port
    
    if client_id:
        CLIENT_ID = client_id
    client = mqtt.Client(CLIENT_ID, clean_session=False)
    client.tls_set(certifi.where())
    client.will_set(CLIENT_ID+"/status", "offline", qos=1, retain=True)
    client.reconnect_delay_set(min_delay=1, max_delay=8)
    client.message_retry_set(5)
    
    mqtt_broker_url = url
    mqtt_broker_port = port
    mqtt_broker_user = username
    mqtt_broker_pw = pw
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.username_pw_set(mqtt_broker_user, mqtt_broker_pw)
    client.connect_async(mqtt_broker_url, mqtt_broker_port, keepalive=4)
    client.loop_start()
