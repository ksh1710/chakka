class Config:
    # Secret key for sessions and CSRF protection
    SECRET_KEY = 'your_secret_key_here'
    
    # Firebase configuration
    FIREBASE_CREDENTIALS = r"path to json folder"
    FIREBASE_DATABASE_URL = 'https://pressure-monitoring-b592a-default-rtdb.firebaseio.com/'
    
    # Debug settings
    DEBUG = True