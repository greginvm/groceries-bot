from bobo import settings
from bobo import db

LIST_KWS = ('list', 'get')
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
    list_ = settings.DEFAULT_LIST

    if _matches_intent(text, HELP_KWS):
        return help_(text, user)
    if _matches_intent(text, ADD_KWS):
        return add(team, list_, text, user)
    elif _matches_intent(text, LIST_KWS):
        return get_all(team, list_, text, user)
    return handle_unknown(user, text)


def get_all(team, list_, text, user):
    items = db.list_(team, list_)

    lines = []
    for _, x in items.iteritems():
        added = u"  (added by _{}_)".format(x['user']) if x.get('user') else u''
        lines.append({
            'text': u"*{}*{}".format(x['name'], added),
            'mrkdwn_in': ['text'],
        })

    return respond(user, "Currently in the shopping list:", text, lines)


def help_(text, user):
    return respond(user, "Bobo understands the following commands:", text, [
        {
            "text": "add X ...",
        },
        {
            "text": "list ...",
        },
        {
            "text": "help",
        },
    ])


def add(team, list_, text, user):
    if _matches_intent(text, VEGAN_KWS):
        return respond(user, u"Vegetables have feelings too!", text)

    entity = _get_entity(text, ADD_KWS)
    if not entity:
        return handle_unknown(user, text)

    db.add(team, list_, {
        'name': entity,
        'user': user,
    })

    return respond(user, u"{} added, thanks {}".format(entity, user), text)


def handle_unknown(user, text):
    return respond(user, "I don't understand that", text)


def respond(user, title, question, attachments=None, response_type="in_channel"):
    if not attachments:
        attachments = []

    # attachments.append({
    #     "color": "36a64f",
    #     "text": "Command by {}: _'{}'_".format(user, question),
    # })

    return {
        "response_type": response_type,
        "text": title,
        "attachments": attachments,
    }
