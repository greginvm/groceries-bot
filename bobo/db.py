import pyrebase
import settings

firebase = pyrebase.initialize_app(settings.FIREBASE)
db = firebase.database()
