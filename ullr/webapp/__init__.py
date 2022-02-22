import flask
import flask_socketio
import logging
import webbrowser
import click

PORT = 5000
webapp = flask.Flask(__name__)
webapp.app_context().push()
socketio = flask_socketio.SocketIO(webapp)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# turn off werkzeug startup printing to the console
def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass


def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass


click.echo = echo
click.secho = secho


def port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def enough_memory():
    import psutil
    memory = round(psutil.virtual_memory().total / (1024.0 ** 3))
    return memory > 2


def run(port=PORT, nopopup=False):
    if (not nopopup) and enough_memory():
        webbrowser.open(f"http://localhost:{port}", new=1)
    if not port_in_use(port):
        print(f"Ullr started on localhost:{port}")
        socketio.run(webapp, host="0.0.0.0", port=port)
    else:
        print(f"Ullr already running on localhost:{port}")
