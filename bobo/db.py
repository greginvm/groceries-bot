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


def add(team, listname, item):
    db = connect().database()

    team = db.child('teams').child(team)
    l = db.child('lists').child(listname)
    l.push(item)


def list_(team, listname):
    db = connect().database()

    return db.child('teams').child(team).child('lists').child(listname).get().val()


def item_exists(name, team, listname):
    items = list_(team, listname)

    if items is not None:
        for _, x in items.iteritems():
            if x['name'] == name:
                return x
    return None


def clear(team, listname):
    db = connect().database()
    return db.child('teams').child(team).child('lists').child(listname).remove()
