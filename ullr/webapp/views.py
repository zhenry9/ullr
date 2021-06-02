import socket
import json
from datetime import date, datetime

from flask import (redirect, render_template, request, Response)

from .. import __version__ as version
from .. import utils
from ..local_device import LocalDevice
from ..remote_device import RemoteDevice
from . import socketing, webapp, socketio
from ..skiracetiming.translate import DECODE, ENCODE
from .. import mqtt_client

current_session = object()


def init(session):
    global current_session
    current_session = session

@webapp.route("/")
def home():
    return render_template(
        "home.html",
        version=version,
        session=current_session,
        ports=utils.get_available_com_ports(),
        hostname=socket.gethostname(),
        host_ip=utils.get_ip(),
        config_file=current_session.config_file.replace("\\", "\\\\"),
        translation_sources=DECODE.keys(),
        translation_destinations=ENCODE.keys(),
        client_id=mqtt_client.CLIENT_ID,
        client_online=mqtt_client.connected,
        broker_url=mqtt_client.mqtt_broker_url,
        broker_port=mqtt_client.mqtt_broker_port,
        broker_user=mqtt_client.mqtt_broker_user,
        broker_pw=mqtt_client.mqtt_broker_pw,
    )


@webapp.route("/add_local", methods=["GET", "POST"])
def add_local():
    if request.method == "POST":
        form = request.form
        mute = False
        incoming = False
        published = False
        if form.get("mute"):
            mute = True
        if form.get("incoming"):
            incoming = True
        if form.get("publish"):
            published = True
        try:
            dev = LocalDevice(
                form["port"],
                form["mode"],
                name=form["name"],
                mute=mute,
                accepts_incoming=incoming,
                baudrate=int(form["baud"]),
                published=published)
            current_session.bus.add_device(dev)
        except Exception as e:
            utils.print_to_ui(f"Failed to add device: {e}")

    return redirect("/")


@webapp.route("/add_remote", methods=["GET", "POST"])
def add_remote():
    if request.method == "POST":
        form = request.form
        mute = False
        incoming = False
        if form.get("mute"):
            mute = True
        if form.get("incoming"):
            incoming = True

        try:
            dev = RemoteDevice(
                form["topic_name"],
                form["mode"],
                name=form["name"],
                accepts_incoming=incoming,
                mute=mute,
                on_time_max=form["on_time_max"]
            )
            current_session.bus.add_device(dev)
        except Exception as e:
            utils.print_to_ui(f"Failed to add device: {e}")

    return redirect("/")


@webapp.route("/remove/<device>", methods=["GET", "POST"])
def remove_device(device):
    current_session.bus.remove_device(device)
    return redirect("/")


@webapp.route("/get_log", methods=["GET", "POST"])
def get_log():
    with open(utils.get_log_file(), "r") as file:
        log = file.read()
    utils.print_to_ui("Served logfile.")
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Response(
        log,
        mimetype="text/plain",
        headers={
            "Content-disposition": f"attachment; filename={now}-ullr-{socket.gethostname()}.log"}
    )


@socketio.on("save_config")
def save_config():
    current_session.save_current_to_file()

@socketio.on("update_mqtt")
def update_mqtt(data):
    data = json.loads(data)
    url, user, pw = "", "", ""
    port = 0
    for item in data:
        if item["name"] == "url":
            url = item["value"]
        elif item["name"] == "port":
            port = int(item["value"])
        elif item["name"] == "user":
            user = item["value"]
        elif item["name"]  == "pw":
            pw = item["value"]
    if mqtt_client.client.is_connected():
        mqtt_client.client.disconnect()
    mqtt_client.start_client(url=url, port=port, username=user, pw=pw)


@socketio.on("update_translation")
def update_translation(id, data):
    data = json.loads(data)
    if data[0]["value"].upper() == "TRUE":
        translation = [
            True,
            data[1]["value"],
            data[2]["value"],
            int(data[3]["value"])
        ]
    else:
        translation = [
            False,
            None,
            None,
            0
        ]
    current_session.bus.update_translation(id, translation)

@socketio.on("update_device")
def update_device(id, data):
    data = json.loads(data)
    d = current_session.bus.find_device(id)
    mute, incoming, publish = False, False, False
    for item in data:
        if item["value"] == "on":
            if item["name"] == "mute":
                mute = True
            elif item["name"] == "incoming":
                incoming = True
            elif item["name"] == "publish":
                publish = True
    d.mute = mute
    d.accepts_incoming = incoming
    if d.type == "serial":
        d.published = publish

@socketio.on("update_ota")
def update_ota(id, data):
    d = current_session.bus.find_device(id)
    data = json.loads(data)
    ota = int(data[0]["value"])
    d.on_time_max = ota
    
@socketio.on("send_late_messages")
def send_late_messages(id, data):
    d = current_session.bus.find_device(id)
    data = json.loads(data)
    index_list = []
    for item in data:
        try:
            index_list.append(int(item["value"]))
        except:
            pass
    d.accept_late_messages(message_index_list=index_list)
    socketio.emit("update_late_messages", id)