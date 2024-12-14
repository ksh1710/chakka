# File: app/firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore, db
import os

# Initialize Firebase
def init_firebase():
   

    cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), '..', 'pressure-monitoring-b592a-firebase-adminsdk-q39g4-c7b8f46072.json'))
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://pressure-monitoring-b592a-default-rtdb.firebaseio.com/'
    })
    return firestore.client(), db.reference()
