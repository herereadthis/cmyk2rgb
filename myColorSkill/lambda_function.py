"""My Color Skill."""

from __future__ import print_function
from distutils.util import strtobool

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
    'welcome_new': {
        'card_title': 'Welcome',
        'speech_output': """
            Welcome to a new session of the color fox. Tell me your favorite
            color.
            """,
        'reprompt_text': """
            Please tell me your favorite color by saying, something like my
            favorite color is red.
            """,
        'should_end_session': False
    },
    'welcome_continue': {
        'card_title': 'Welcome',
        'speech_output': """
            Let\'s continue your current session of the color fox. Last time,
            your favorite color was {}. Please choose a new color.
            """,
        'reprompt_text': """
            Please pick a new color by saying something like my favorite color
            is red.
            """,
        'should_end_session': False
    },
    'end_session_known_color': {
        'card_title': 'Session Ended',
        'speech_output': """
            Thank you for playing the color fox. I hope your day is full of
            many {0} things and {1} foods!
            """,
        'reprompt_text': None,
        'should_end_session': True
    },
    'end_session_unknown_color': {
        'card_title': 'Session Ended',
        'speech_output': """
            Thank you for playing the color fox. Have a nice day!
            """,
        'reprompt_text': None,
        'should_end_session': True
    },
    'continue_end_ambituity': {
        'card_title': 'ContinueEndAmbiguity',
        'speech_output': """
            I\'m not sure what you want.
            """,
        'reprompt_text': None,
        'should_end_session': True
    },
    'continue_session': {
        'card_title': 'ContinueSessionIntent',
        'speech_output': """
            I\'m not sure what you want.
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
        'speech_output': """
            Your favorite color is {}. Would you like to continue?
            """,
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
            I'm sorry, I don't think I know that color. Please pick another
            color.
            """,
        'reprompt_text': None,
        'should_end_session': False
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


def build_unformatted_speechlet_response(response_type):
    """Build a basic response that does not require formatting."""
    try:
        responses = RESPONSES[response_type]
    except:
        responses = RESPONSES['help']

    card_title = responses['card_title']
    speech_output = responses['speech_output']
    reprompt_text = responses['reprompt_text']
    # Setting this to true ends the session and exits the skill.
    should_end_session = responses['should_end_session']

    response = get_response(card_title, speech_output, reprompt_text,
                            should_end_session)
    return get_lambda_output(response)


def get_response_alt(response_type, **kwargs):
    """Create the response for Alexa to interpret."""
    try:
        responses = RESPONSES[response_type]
        speech_output = responses['speech_output']
        reprompt_text = responses['reprompt_text']
        if 'speech_output' in kwargs:
            speech_output = kwargs['speech_output']
        if 'reprompt_text' in kwargs:
            reprompt_text = kwargs['reprompt_text']
    except:
        responses = RESPONSES['help']
        speech_output = responses['speech_output']
        reprompt_text = responses['reprompt_text']

    responses = RESPONSES[response_type]
    card_title = responses['card_title']
    should_end_session = responses['should_end_session']

    return get_response(card_title, speech_output, reprompt_text,
                        should_end_session)


def get_response(title, output, reprompt_text, should_end_session):
    """Create the response for Alexa to interpret."""
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - {}'.format(title),
            'content': 'SessionSpeechlet - {}'.format(output)
        },
        # If the user either does not reply to the welcome message or says
        # something that is not understood, they will be prompted again with
        # this text.
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                # Setting reprompt_text to None signifies that we do not want
                # to reprompt the user. If the user does not respond or says
                # something that is not understood, the session will end.
                'text': reprompt_text
            }
        },
        # Setting this to true ends the session and exits the skill.
        'shouldEndSession': should_end_session
    }


def get_lambda_output(response, session_attributes={}):
    """Construct the JSON output for the lambda function."""
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': response
    }


# --------------- Functions that control the skill's behavior -----------------


def handle_welcome(request, session):
    """Create the welcome response."""
    return build_unformatted_speechlet_response('welcome_new')


def handle_restart_session(request, session):
    """Create a welcome response to continue session."""
    try:
        favorite_color = session['attributes']['favoriteColor']
        output = RESPONSES['welcome_continue']['speech_output']
        output = output.format(favorite_color, favorite_color)

        response = get_response_alt('set_known_color', speech_output=output)
        result = get_lambda_output(response)
    except KeyError:
        result = build_unformatted_speechlet_response('help')

    return result


def handle_session_end_request(intent, session):
    """Create the response when ending exiting the app."""
    try:
        favorite_color = session['attributes']['favoriteColor']
        output = RESPONSES['end_session_known_color']['speech_output']
        output = output.format(favorite_color, favorite_color)

        response = get_response_alt('end_session_known_color',
                                    speech_output=output)
        return get_lambda_output(response)
    except KeyError:
        return build_unformatted_speechlet_response(
            'end_session_unknown_color')


def handle_help_request():
    """Create the response user asks for help."""
    return build_unformatted_speechlet_response('help')


def handle_continue_end_ambiguity_request(intent, session):
    """Create response when user says yes or no at the wrong time."""
    # TODO: handle yes and no.
    return build_unformatted_speechlet_response('continue_end_ambituity')


def handle_yes_request(intent, session):
    """Create the response when the user says yes."""
    result = handle_continue_end_ambiguity_request(intent, session)
    try:
        continue_prompt_asked = session['attributes']['continuePromptAsked']
        if strtobool(continue_prompt_asked) == 1:
            result = handle_restart_session(intent, session)
    except KeyError:
        pass

    return result


def handle_no_request(intent, session):
    """Create the response when the user says no."""
    try:
        favorite_color = session['attributes']['favoriteColor']
        continue_prompt_asked = session['attributes']['continuePromptAsked']
        if strtobool(continue_prompt_asked) == 1:
            result = handle_session_end_request(intent, session)
        else:
            session_attributes = {}
            card_title = 'EndSessionIntent'
            speech_output = 'no no no {}'.format(favorite_color,
                                                 continue_prompt_asked)
            reprompt_text = None
            should_end_session = True

            response = get_response(card_title, speech_output, reprompt_text,
                                    should_end_session)
            result = get_lambda_output(response, session_attributes)
    except KeyError:
        result = handle_continue_end_ambiguity_request(intent, session)

    return result


def set_color_in_session(intent, session):
    """Set the color in the session and prepare the reply speech to user."""
    if 'Color' in intent['slots']:
        color = intent['slots']['Color']
        favorite_color = color['value']
        resolutions = color['resolutions']
        resolutions_per_authority = resolutions['resolutionsPerAuthority'][0]
        code = resolutions_per_authority['status']['code']

    if code == CODES['match']:
        session_attributes = create_favorite_color_attributes(favorite_color)

        output = RESPONSES['set_known_color']['speech_output']
        output = output.format(favorite_color)

        response = get_response_alt('set_known_color', speech_output=output)
        result = get_lambda_output(response, session_attributes)
    elif code == CODES['no_match']:
        result = build_unformatted_speechlet_response('set_unknown_color')

    return result


def get_color_from_session(intent, session):
    """Respond to WhatsMyColorIntent request."""
    try:
        favorite_color = session['attributes']['favoriteColor']

        output = RESPONSES['get_known_color']['speech_output']
        output = output.format(favorite_color)

        response = get_response_alt('get_known_color', speech_output=output)
        session_attributes = create_continue_prompt_attributes(favorite_color)
        result = get_lambda_output(response, session_attributes)
    except KeyError:
        result = build_unformatted_speechlet_response('get_unknown_color')

    return result


def create_favorite_color_attributes(favorite_color):
    """Add favorite color to session attributes."""
    return {
        "favoriteColor": favorite_color
    }


def create_continue_prompt_attributes(favorite_color):
    """Add favorite color to session attributes."""
    try:
        attributes = create_favorite_color_attributes(favorite_color)
    except:
        attributes = create_favorite_color_attributes(None)

    attributes['continuePromptAsked'] = 'True'
    return attributes


# --------------- Events ------------------

def on_session_started(request, session):
    """Call when the session starts."""
    request_id = request['requestId']
    session_id = session['sessionId']

    output = 'on_session_started requestId={0}, sessionId={1}'
    print(output.format(request_id, session_id))


def on_launch(request, session):
    """Launch the skill without the user specifying what they want."""
    # Dispatch to your skill's launch
    return handle_welcome(request, session)


def on_intent(request, session):
    """Call when the user specifies an intent for this skill."""
    request_id = request['requestId']
    session_id = session['sessionId']

    output = 'on_intent requestId={0}, sessionId={1}'
    print(output.format(request_id, session_id))

    intent = request['intent']
    intent_name = intent['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.CancelIntent":
        return handle_session_end_request(intent, session)
    elif intent_name == "AMAZON.StopIntent":
        return handle_session_end_request(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_help_request()
    elif intent_name == "ContinueSessionIntent":
        return handle_yes_request(intent, session)
    elif intent_name == "EndSessionIntent":
        return handle_no_request(intent, session)
    elif intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(request, session):
    """Called when the user ends the session."""
    # Is not called when the skill returns should_end_session=true
    print("on_session_ended requestId=" + request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here
    return handle_session_end_request(request['intent'], session)


def lambda_handler(event, context):
    """Main Handler skill."""
    # Route the incoming request based on type (LaunchRequest, IntentRequest,
    # etc.) The JSON body of the request is provided in the event parameter.

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
        # If we wanted to initialize the session to have some attributes, we
        # could add those here.
        on_session_started(event['request'], event['session'])

    event_type = event['request']['type']

    if event_type == "LaunchRequest":
        handler = on_launch
    elif event_type == "IntentRequest":
        handler = on_intent
    elif event_type == "SessionEndedRequest":
        handler = on_session_ended

    return handler(event['request'], event['session'])
