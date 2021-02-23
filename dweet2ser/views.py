
from . import settings
from .local_device import LocalDevice
from .remote_device import RemoteDevice
from flask import Flask, render_template, request, redirect, Response, stream_with_context

from . import webapp

bus = object()
cfg = object()

def init(bus_from_main, cfg_from_main):
    global bus
    bus = bus_from_main
    cfg = cfg_from_main

def stream_template(template_name, **context):
    webapp.update_template_context(context)
    t = webapp.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

@webapp.route("/")
def home():
    
    console_buffer = settings.get_console_buffer()
    return render_template(
        "home.html",
        console=console_buffer,
        bus=bus,
        cfg=cfg,
        file=settings.DEFAULT_CONFIG_FILE,
        ports=settings.get_available_com_ports()
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
            bus.add_device(dev)
        except Exception as e:
            settings.print_to_web_console(f"{settings.timestamp()}Failed to add device: {e}")
    
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
            bus.add_device(dev)
        except Exception as e:
            settings.print_to_web_console(f"{settings.timestamp()}Failed to add device: {e}")
    
    return redirect("/")
