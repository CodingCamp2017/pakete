from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement

import urllib.request

packets = [
'da0dff7b-4adb-4dcc-b9cc-9943e39c8248', 
'698c9809-dc10-47f5-a2a6-856d8cc7a07e', 
'd5fe37c2-e1c7-486c-8daf-43f7589394de',
'79954bed-b983-4f4a-9a4d-ae03dfe4fc77',
'595ca835-055a-4fed-a33c-a437e68de9e6',
'192dd852-b0a0-4679-ad7d-58a40e07a0a5',
'5ee70a06-11d5-4198-b8d0-7812a1aa21b2'
]

BASE_URL = 'http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8001'


app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def launch():
    welcome_text = render_template('welcome')
    help_text = render_template('help')
    return question(welcome_text).reprompt(help_text)

@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = render_template('help')
    return statement(help_text).simple_card('Hilfe', help_text)

@ask.intent('AMAZON.StopIntent')
def stop():
    stop_text = render_template('stop')
    return statement(stop_text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    stop_text = render_template('stop')
    return statement(stop_text)

@ask.intent('StartTrackingIntent')
def start_track():
    get_packet_number_text = render_template('get_packet_number')
    return question(get_packet_number_text)

@ask.intent('TrackingIntent', convert={'packet_number': int})
def track(packet_number):
    packet_info = get_packet_info(packet_number)
    if not packet_info:
        error_text = render_template('error')
        help_text = render_template('help')
        return question(error_text).reprompt(help_text)
    packet_info = json.loads(packet_info)
    if 'deliveryTime' in packet_info:
        already_delivered_text = render_template('already_delivered')
        return question(already_delivered_text)
    elif not packet_info['stations']:
        just_sent_text = render_template('just_sent')
        return question(just_sent_text)
    else:
        current_city = packet_info['stations'][-1]['location']
        packet_located_at_text = render_template('packet_located_at', city=current_city)
        return question(packet_located_at_text)

def get_packet_info(packet_number):
    if packet_number > len(packets):
        return None
    packet_number = packets[packet_number-1]
    request = urllib.request.Request(BASE_URL + '/packetStatus/' + packet_number)
    response = urllib.request.urlopen(request)
    responseJson = json.loads(response.read().decode('utf8'))
    return responseJson

if __name__ == '__main__':
    app.run()