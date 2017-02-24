import random

from bobo import db
from bobo import settings

VEGAN_RESPONES = [
    'No, who would even eat {item}',
    'Vegetables have feelings too!',
    'What is even {item}',
    'Shopping list full',
    'Bag full',
]


def get_list(intent, session):
    team = settings.DEFAULT_TEAM
    list_ = settings.DEFAULT_LIST
    items = db.list_(team, list_)
    if not items:
        return 'List is empty', None, {}
    return 'Currently in the list: ' + ', '.join(itm['name'] for itm in items.itervalues()), None, {}


def set_item(intent, session):
    team = settings.DEFAULT_TEAM
    list_ = settings.DEFAULT_LIST

    item = intent['slots']['Item']['value']
    if 'vegan ' in item:
        return random.choice(VEGAN_RESPONES).format(item=item), None, {}
    if db.item_exists(item, team, list_):
        return '{} is already on the list'.format(item), None, {}
    db.add(team, list_, {
        'name': item,
        'user': '',
    })

    return 'Item added', None, {}


def clear_list(intent, session):
    return 'Are you sure you want to clear the shopping list?', None, {
        'action': 'ClearList'
    }


def clear_list_continue(intent, session):
    clear_list_exists = session.get('attributes').get('action') == 'ClearList'
    if clear_list_exists and intent['name'] == "AMAZON.YesIntent":
        team = settings.DEFAULT_TEAM
        list_ = settings.DEFAULT_LIST
        db.clear(team, list_)
        return 'Shopping list cleared', None, {}
    if clear_list_exists and intent['name'] == "AMAZON.YesIntent":
        return 'OK, should I start ignoring you?.', None, {}
    return 'Stop, you will mess things up.', None, {}
