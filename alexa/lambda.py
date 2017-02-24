import handler
import common

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetList":
        response, reprompt, session = handler.get_list(intent, session)
        return common.build_response(
            session,
            common.build_speechlet_response('List all groceries', response, reprompt or response)
        )
    elif intent_name == "SetItem":
        response, reprompt, session = handler.set_item(intent, session)
        return common.build_response(
            session,
            common.build_speechlet_response('Item set', response, reprompt or response)
        )
    else:
        raise ValueError("Invalid intent")

def lambda_handler(event, context):
    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if event['session']['application']['applicationId'] not in handler.settings.ALEXA_IDS:
        raise ValueError("Invalid Application ID")

    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
