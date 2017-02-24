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

    if _matches_intent(text, ADD_KWS):
        return add(team, list_, text, user)
    elif _matches_intent(text, LIST_KWS):
        return get_all(team, list_)
    return handle_unknown(user, text)


def get_all(team, list_):
    items = db.list_(team, list_)

    lines = []
    for _, x in items.iteritems():
        added = u" (added by {})".format(x['user']) if x.get('user') else u''
        lines.append(
            u"{}{}".format(x['name'], added)
        )

    return u"""
    Currently in the shopping list:
    {}
    """.format(u"\n".join(lines))


def add(team, list_, text, user):
    if _matches_intent(text, VEGAN_KWS):
        return u"Vegetables have feelings too!"

    entity = _get_entity(text, ADD_KWS)
    if not entity:
        return u"I don't understand that"

    db.add(team, list_, {
        'name': entity,
        'user': user,
    })

    return u"{} added, thanks {}".format(entity, user)


def handle_unknown(user, text):
    return u"{}, I don't understand '{}'".format(user, text)
