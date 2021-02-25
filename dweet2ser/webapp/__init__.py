import flask
import flask_socketio

webapp = flask.Flask(__name__)
webapp.app_context().push()
socketio = flask_socketio.SocketIO(webapp)