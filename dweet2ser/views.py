
from . import settings
from flask import Flask, render_template

from . import webapp

bus = object()
cfg = object()

def init(bus_from_main, cfg_from_main):
    global bus
    bus = bus_from_main
    cfg = cfg_from_main

@webapp.route("/")
def home():
    return render_template(
        "home.html",
        console=settings.get_console_buffer(),
        bus=bus,
        cfg=cfg,
        file=settings.DEFAULT_CONFIG_FILE
    )