import flask
import flask_socketio


__version__ = '0.1.3'

webapp = flask.Flask(__name__)
webapp.app_context().push()
socketio = flask_socketio.SocketIO(webapp)
