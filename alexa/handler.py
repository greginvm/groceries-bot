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
    db.add(team, list_, {
        'name': item,
        'user': '',
    })
    
    return 'Item added', None, {}
