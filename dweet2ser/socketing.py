

from . import socketio
from .settings import timestamp

WEB_CONSOLE_BUFFER = '\r'
TAPES ={}

def print_to_web_console(message, endline = "\n"):
    """Thread safe print function"""
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

@socketio.on("connect")
def on_connect():
    load_tapes()
    print_to_web_console(f"{timestamp()}Connected to web client.")