import flask
import flask_socketio
import logging

webapp = flask.Flask(__name__)
webapp.app_context().push()
socketio = flask_socketio.SocketIO(webapp)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def run():
    socketio.run(webapp, host="0.0.0.0")