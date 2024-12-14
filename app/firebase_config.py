# File: app/firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore, db
import os
from flask_socketio import SocketIO

# Initialize Firebase
def init_firebase():
   
    cred = credentials.Certificate("sihCreds.json")
    # cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), '..', 'path to json folder'))
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://pressure-monitoring-b592a-default-rtdb.firebaseio.com/'}
    )
    return firestore.client(), db.reference()

