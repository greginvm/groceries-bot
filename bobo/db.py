import pyrebase
import settings

class Model:
    def connect(self):
        if self.db:
            return
        self.firebase = pyrebase.initialize_app(settings.FIREBASE)
        self.db = self.firebase.database()
  
    def __init__(self):
        self.db = None

