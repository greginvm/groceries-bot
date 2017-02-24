from bobo import settings
from bobo import db

LISTNAMEKWS = ('list', 'get')
ADD_KWS = ('add', 'put', 'post')
STRIP_WORDS = (
    'to', 'what', 'who',
    'or', 'and',
    'shopping', 'groceries', 'list',
    'a', 'an', 'the', 'bobo', 'what', 'is', 'are', 'i', 'am'
)

VEGAN_KWS = (
    'soya', 'soy', 'vegan', 'vege', 'vegi'
)
HELP_KWS = {
    '?', 'help', 'man'
}

def _matches_intent(text, kws):
    return any(x in text.split() for x in kws)


def _space(kws):
    return [' {} '.format(x.lower()) for x in kws]


def _get_entity(text, cmd_kws):
    words = text.lower().split()
    strip = cmd_kws + STRIP_WORDS
    entities = [x for x in words if x not in strip]
    if entities:
        return " ".join(entities)
    return ""


def trigger(user, text):
    team = settings.DEFAULT_TEAM
    listname = settings.DEFAULT_LIST

    if _matches_intent(text, HELP_KWS):
        return help_()
    if _matches_intent(text, ADD_KWS):
        return add(team, listname, text, user)
    elif _matches_intent(text, LISTNAMEKWS):
        return get_all(team, listname)
    return handle_unknown()


def get_all(team, listname):
    items = db.list_(team, listname)

    if not items:
        return response("Nothing on the list yet")

    lines = []
    for _, x in items.iteritems():
        added = u"  (added by _{}_)".format(x['user']) if x.get('user') else u''
        lines.append({
            'text': u"*{}*{}".format(x['name'], added),
            'mrkdwn_in': ['text'],
        })

    return response("Currently on the shopping list:", lines)


def help_():
    return response("Bobo understands the following commands:", [
        {"text": "add X ...",},
        {"text": "list ...",},
        {"text": "help",},
    ])


def add(team, listname, text, user):
    if _matches_intent(text, VEGAN_KWS):
        return response(u"Vegetables have feelings too! Nothing added")

    entity = _get_entity(text, ADD_KWS)
    if not entity:
        return handle_unknown()

    existing = db.item_exists(entity, team, listname)
    if existing:
        return response("This item was already added by {}, thanks anyway".format(existing['user']))

    db.add(team, listname, {
        'name': entity,
        'user': user,
    })

    return response(u"{} added, thanks {}".format(entity, user))



def handle_unknown():
    return response("I'm a simple piggy, I don't understand that, try harder")


def response(title, attachments=None, response_type="in_channel"):
    if not attachments:
        attachments = []

    return {
        "response_type": response_type,
        "text": title,
        "attachments": attachments,
    }
