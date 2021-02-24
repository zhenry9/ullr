import flask
import flask_socketio


__version__ = '0.2.0'

webapp = flask.Flask(__name__)
webapp.app_context().push()
socketio = flask_socketio.SocketIO(webapp)
