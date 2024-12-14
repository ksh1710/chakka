# import eventlet
# eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO

import app.routes as routes
# from app import create_app,socketio

socketio = SocketIO()

if __name__ == '__main__':
    app = Flask(__name__)
    routes.init_routes(app)
    # app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)