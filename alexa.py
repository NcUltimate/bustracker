"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import urllib, httplib, json, re


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_error_response(intent, error):
    reprompt_text = "You can ask things like, when is the next northbound " \
                    "151 bus from Union Station"
    return build_response({}, build_speechlet_response(
        'Your bus request could not be made.', error, reprompt_text, True))

def get_default_response():
    card_title = "Welcome"
    speech_output = "Sorry, I didn't understand that. You can ask things " \
                    "like, when is the next northbound 151 bus from "\
                    "Union Station"
    reprompt_text = "You can ask things like, when is the next northbound " \
                    "151 bus from Union Station"
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))

def get_welcome_response():
    card_title = "Welcome"
    speech_output = "Welcome to the CTA Tracker. You can ask things " \
                    "like, when is the next northbound 151 bus from "\
                    "Union Station"
    reprompt_text = "You can ask things like, when is the next northbound " \
                    "151 bus from Union Station"
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Now closing the CTA Train and Bus Tracker" 
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        

def request_data(data_type, params):
    # First, build the request params
    param_hash = {'key' : 'U529bPGQWxNMg85yPuDFm5nn3', 'format' : 'json'}
    param_hash.update(params)
    params = urllib.urlencode(param_hash)
    
    # Then, make the request
    conn = httplib.HTTPConnection("www.ctabustracker.com")
    conn.request("GET", "/bustime/api/v2/" + data_type + "?" + params)
    response = conn.getresponse()
    
    # Return the request data JSON if successful
    if response.status == 200:
        output = json.loads(response.read())
        if 'bustime-response' in output:
            output = output['bustime-response']
        else:
            output = {}
    else:
        output = {}
    conn.close()
    return output

def sanitize_stop_name(sname):
  sname = sname.lower()
  sname = re.sub('&', 'and', sname)
  sname = re.sub("\bn\.?\b", 'north', sname)
  sname = re.sub("\bs\.?\b", 'south', sname)
  sname = re.sub("\be\.?\b", 'east', sname)
  sname = re.sub("\bw\.?\b", 'west', sname)
  sname = re.sub("\bave\.?\b", 'avenue', sname)
  sname = re.sub("\bblvd\.?\b", 'boulevard', sname)
  sname = re.sub("\bctr\.?\b", 'center', sname)
  sname = re.sub("\bst\.", 'saint', sname)
  sname = re.sub("-", ' ', sname)
  sname = re.sub(" ", '', sname)
  return sname

def get_predictions(bus_route, stop_id):
    preds = request_data('getpredictions', { 'rt' : bus_route, 'stpid' : stop_id })
    if 'error' in preds or 'prd' not in preds:
        return []

    return map(lambda p: p['prdctdn'], preds['prd'])

def get_stop_id_and_name(bus_route, drctn, bus_stop):
    stops = request_data('getstops', { 'rt' : bus_route, 'dir' : drctn })
    if 'error' in stops or 'stops' not in stops:
        return None, None

    bus_stop = sanitize_stop_name(bus_stop)
    for stop in stops['stops']:
        stop_nm = sanitize_stop_name(stop['stpnm'])
        if bus_stop in stop_nm:
            return stop['stpid'], stop['stpnm']
    return None, None

def get_directions(bus_route, drctn):
    possible = request_data('getdirections', { "rt" : bus_route } )
    if 'error' in possible or 'directions' not in possible:
        return []

    drctns = map(lambda p: p['dir'].capitalize(), possible['directions'])
    return [drctn.capitalize()] if drctn and drctn.capitalize() in drctns else drctns

def get_prediction_response(intent, drctn, bus_route, bus_stop, predictions):
    ret_val = "The next " + drctn + ' ' + bus_route + ' bus will depart from ' + bus_stop + " in "

    predictions = filter(lambda p: p != 'DLY', predictions)
    predictions = map(lambda p: int(p) if p[0].isdigit() else 0, predictions)
    predictions = list(set(predictions))
    predictions.sort()

    k = 0
    for p in predictions:
        k += 1
        if p == 0:
            ret_val = ret_val + 'less than 1 minute'
        else:
            ret_val = ret_val + str(p) + " minutes"

        if k < len(predictions) - 1:
            ret_val = ret_val + ', '
        elif k == len(predictions) - 1 and len(predictions) != 1:
            ret_val = ret_val + ', and '
    ret_val = ret_val + '.'
    return build_response({}, build_speechlet_response(
        'Your upcoming bus information', ret_val, None, True))

def get_bus_response(intent, session):
    if 'slots' not in intent:
        return get_default_response()
    if 'BusStop' not in intent['slots'] or 'value' not in intent['slots']['BusStop']:
        return get_default_response()  
    if 'BusDirection' not in intent['slots']:
        return get_default_response()   
    if 'Route' not in intent['slots'] or 'value' not in intent['slots']['Route']:
        return get_default_response()     

    bus_stop = intent['slots']['BusStop']['value']
    bus_route = intent['slots']['Route']['value']
    direction = None if 'value' not in intent['slots']['BusDirection'] else intent['slots']['BusDirection']['value']

    directions = get_directions(bus_route, direction)
    stop_id = None
    stop_name = None
    for drctn in directions:
        stop_id, stop_name = get_stop_id_and_name(bus_route, drctn, bus_stop)
        if stop_id:
            direction = drctn
            break

    if stop_id == None:
        direction = ''
        return get_error_response(intent,
            "Sorry, I couldn't find any " + direction + " " +
            bus_route + " stops named '" + bus_stop + "'")

    predictions = get_predictions(bus_route, stop_id)
    if len(predictions) == 0:
        return get_error_response(intent, 'There are no upcoming ' + direction + ' ' + bus_route + ' buses through ' + bus_stop + '.')

    return get_prediction_response(intent, direction, bus_route, stop_name, predictions)

def get_train_response(intent, session):
    output = "Sorry, trains currently aren't supported."
    return build_response({}, build_speechlet_response(
        'Your train request', output, None, False))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    return get_welcome_response()


def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "BusIntent":
        return get_bus_response(intent, session)
    elif intent_name == "TrainIntent":
        return get_train_response(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# --------------- Main handler ------------------

def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.0f2db0c9-f3ab-4720-91b1-a22cd6957588"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
