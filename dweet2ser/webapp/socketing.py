import datetime

from flask import request

from . import socketio

WEB_CONSOLE_BUFFER = '\r'
TAPES = {}


def timestamp():
    return "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] "


def print_to_web_console(message, endline="\n"):
    global WEB_CONSOLE_BUFFER
    WEB_CONSOLE_BUFFER += str(message) + str(endline)
    socketio.emit("console", WEB_CONSOLE_BUFFER)


def print_tape(target, message):
    message = " ".join(message.split())
    global TAPES
    if TAPES.get(target) is None:
        TAPES[target] = ""
    elif TAPES.get(target) is not str:
        TAPES[target] = str(TAPES[target])
    TAPES[target] += message + "\n"
    payload = {"target": target, "buffer": TAPES[target]}
    socketio.emit("tape_feed", payload)


def load_tapes():
    for tape in TAPES:
        payload = {"target": tape, "buffer": TAPES[tape]}
        socketio.emit("tape_feed", payload)


def update_online_dot(device, online=False):
    payload = {"target": str(device), "online": str(online)}
    socketio.emit("update_online_dot", payload)

def update_late_badge(device, count):
    payload = {"target": str(device), "count": count}
    socketio.emit("update_late_badge", payload)

def update_client_status(online=False):
    payload = {"online": str(online)}
    socketio.emit("update_client_status", payload)

@socketio.on("connect")
def on_connect():
    client_name = request.remote_addr
    load_tapes()
    print_to_web_console(
        f"{timestamp()}Connected to web client: {client_name}.")
