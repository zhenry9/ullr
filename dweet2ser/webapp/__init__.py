import flask
import flask_socketio
import logging
import webbrowser

PORT = 5000
webapp = flask.Flask(__name__)
webapp.app_context().push()
socketio = flask_socketio.SocketIO(webapp)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run():
    webbrowser.open(f"http://localhost:{PORT}", new=1)
    if not port_in_use(PORT):
        socketio.run(webapp, host="0.0.0.0")
