"""My Color Skill."""

from __future__ import print_function

"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

CODES = {
    'match': 'ER_SUCCESS_MATCH',
    'no_match': 'ER_SUCCESS_NO_MATCH'
}

APPLICATION_ID = 'amzn1.ask.skill.a93ba60c-e4f2-42a5-b08a-f5b8ddbf6f44'

RESPONSES = {
    'welcome': {
        'card_title': 'Welcome',
        'speech_output': """
            {} the color fox 4. Tell me your favorite color.
            """,
        'reprompt_text': """
            Please tell me your favorite color by saying, something like my
            favorite color is red.
            """,
        'should_end_session': False,
        'custom_data': {
            'new_session_text': 'Welcome to a new session of',
            'current_session_text': 'Let\'s continue your current session of'
        }
    },
    'end_session': {
        'card_title': 'Session Ended',
        'speech_output': """
            Thank you for playing the color fox. Have a nice day!
            """,
        'reprompt_text': None,
        'should_end_session': True
    },
    'help': {
        'card_title': 'Session Help',
        'speech_output': """
            I'm interested in your favorite color. You can tell me your
            favorite color by saying something like, "it's blue."
            """,
        'reprompt_text': """
            Everyone has a favorite color. Please tell me yours by saying
            something like, "it's blue."
            """,
        'should_end_session': False
    },
    'get_known_color': {
        'card_title': 'WhatsMyColorIntent',
        'speech_output': 'Your favorite color is {}. Goodbye.',
        'reprompt_text': """
            You can ask me your favorite color by saying, what's my favorite
            color?
            """,
        'should_end_session': False
    },
    'get_unknown_color': {
        'card_title': 'WhatsMyColorIntent',
        'speech_output': """
            I'm not sure what your favorite color is. You can say, my favorite
            color is red.
            """,
        'reprompt_text': """
            So um, please tell me your favorite color by saying, something
            like my favorite color is red. {}
            """,
        'should_end_session': False
    },
    'set_unknown_color': {
        'card_title': 'MyColorIsIntent',
        'speech_output': """
            I'm not sure what your favorite color is. Please try again.
            """,
        'reprompt_text': None,
        'should_end_session': True
    },
    'set_known_color': {
        'card_title': 'MyColorIsIntent',
        'speech_output': """
            I now know your favorite color is {}. You can ask me your favorite
            color by saying, what's my favorite color?
            """,
        'reprompt_text': """
            You can ask me your favorite color by saying, what's my favorite
            color?
            """,
        'should_end_session': False
    }
}

# --------------- Helpers that build all of the responses ---------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    """Create the response for Alexa to interpret."""
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                # If the user either does not reply to the welcome message or
                # says something that is not understood, they will be prompted
                # again with this text.
                'text': reprompt_text
            }
        },
        # Setting this to true ends the session and exits the skill.
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior -----------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = """
    Welcome to the color fox 7. Tell me your favorite color.
    Jimmy, you are prettier than your wife Uyen.
    """

    # If the user either does not reply to the welcome message or says
    # something that is not understood, they will be prompted again with this
    # text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    """Create the response when ending exiting the app."""
    responses = RESPONSES['end_session']

    session_attributes = {}
    card_title = responses['card_title']
    speech_output = responses['speech_output']
    reprompt_text = responses['reprompt_text']
    # Setting this to true ends the session and exits the skill.
    should_end_session = responses['should_end_session']

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_help_request():
    """Create the response user asks for help."""
    responses = RESPONSES['help']

    session_attributes = {}
    card_title = responses['card_title']
    speech_output = responses['speech_output']
    reprompt_text = responses['reprompt_text']
    should_end_session = responses['should_end_session']

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        "session" + str(session_attributes) + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.CancelIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.HelpIntent":
        return handle_help_request()
    elif intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """Called when the user ends the session."""
    """
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here
    return handle_session_end_request()


def lambda_handler(event, context):
    """Main Handler skill."""
    """
    Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    application_id = event['session']['application']['applicationId']

    print('event.session.application.applicationId={}'.format(application_id))

    if application_id != APPLICATION_ID:
        """
        Make sure the event's application ID is the same as the skill's
        application ID, to prevent someone else from configuring a skill that
        sends requests to this function.
        """
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    event_type = event['request']['type']

    if event_type == "LaunchRequest":
        handler = on_launch
    elif event_type == "IntentRequest":
        handler = on_intent
    elif event_type == "SessionEndedRequest":
        handler = on_session_ended

    return handler(event['request'], event['session'])
