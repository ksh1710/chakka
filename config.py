class Config:
    # Secret key for sessions and CSRF protection
    SECRET_KEY = 'your_secret_key_here'
    
    # Firebase configuration
    FIREBASE_CREDENTIALS = r"D:\tire_monitoring_system\pressure-monitoring-b592a-firebase-adminsdk-q39g4-c7b8f46072.json"
    FIREBASE_DATABASE_URL = 'https://pressure-monitoring-b592a-default-rtdb.firebaseio.com/'
    
    # Debug settings
    DEBUG = True