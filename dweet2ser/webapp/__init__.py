import flask
import flask_socketio

webapp = flask.Flask(__name__)
webapp.app_context().push()
socketio = flask_socketio.SocketIO(webapp)

def run():
    socketio.run(webapp, host="0.0.0.0")