import pyrebase
import settings

CONNECTION = None

def connect():
    global CONNECTION

    if CONNECTION is None:
        CONNECTION = pyrebase.initialize_app(settings.FIREBASE)
    return CONNECTION


def get_default_item():
    return {
        'name': '',
        'quantity': '',
        'user': None,
    }


def add(team, list_, item):
    db = connect().database()

    team = db.child('teams').child(team)
    list_ = db.child('lists').child(list_)
    list_.push(item)


def remove(team, list_, item):
    # db = connect().database()

    # team = db.child('teams').child(team)
    # list_ = db.child('lists').child(list_)
    # list_.push(item)
    pass


def list_(team, list_):
    db = connect().database()

    return db.child('teams').child(team).child('lists').child(list_).get().val()
