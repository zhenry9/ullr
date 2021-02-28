import socket
from datetime import date, datetime

from flask import (redirect, render_template, request, Response)

from .. import __version__ as version
from .. import utils
from ..local_device import LocalDevice
from ..remote_device import RemoteDevice
from . import socketing, webapp, socketio

current_session = object()

def init(session):
    global current_session
    current_session = session

def stream_template(template_name, **context):
    webapp.update_template_context(context)
    t = webapp.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

@webapp.route("/")
def home():
    return render_template(
        "home.html",
        version=version,
        session=current_session,
        ports=utils.get_available_com_ports(),
        hostname=socket.gethostname(),
        host_ip=utils.get_ip(),
        config_file=current_session.config_file.replace("\\", "\\\\")
    )

@webapp.route("/add_local", methods=["GET", "POST"])
def add_local():
    if request.method == "POST":
        form = request.form
        mute = False
        if form.get("mute"):
            mute = True

        try:
            dev = LocalDevice(
                form["port"], 
                form["mode"], 
                form["name"], 
                mute=mute, 
                baudrate=form["baud"])
            current_session.bus.add_device(dev)
        except Exception as e:
            socketing.print_to_web_console(f"{utils.timestamp()}Failed to add device: {e}")
    
    return redirect("/")

@webapp.route("/add_remote", methods=["GET", "POST"])
def add_remote():
    if request.method == "POST":
        form = request.form
        mute = False
        if form.get("mute"):
            mute = True

        try:
            dev = RemoteDevice(
                form["thing_id"], 
                form["mode"], 
                name=form["name"], 
                mute=mute, 
                )
            current_session.bus.add_device(dev)
        except Exception as e:
            socketing.print_to_web_console(f"{utils.timestamp()}Failed to add device: {e}")
    
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
        headers={"Content-disposition": f"attachment; filename={now}-dweet2ser-{socket.gethostname()}.log"}
    )
@socketio.on("save_config")
def save_config():
    current_session.save_current_to_file()