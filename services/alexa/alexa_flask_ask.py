from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement

import urllib.request
import logging

import threading

packets = [
'da0dff7b-4adb-4dcc-b9cc-9943e39c8248', 
'698c9809-dc10-47f5-a2a6-856d8cc7a07e', 
'd5fe37c2-e1c7-486c-8daf-43f7589394de',
'79954bed-b983-4f4a-9a4d-ae03dfe4fc77',
'595ca835-055a-4fed-a33c-a437e68de9e6',
'192dd852-b0a0-4679-ad7d-58a40e07a0a5',
'5ee70a06-11d5-4198-b8d0-7812a1aa21b2   '
]

TRACKING_BASE_URL = 'http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8001'
USER_BASE_URL = 'http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8002'

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
ask = Ask(app, '/')

class AlexaPacketTrackingData:
    def __init__(self, email='', password=''):
        self.email = email
        self.password = password
        self.sessionId = ''
        self.packetIds = list()
        self.packetsVerbose = list()

    def setSessionId(self, sessionId):
        self.sessionId = sessionId

    def setPacketIds(self, packetIds):
        self.packetIds = packetIds

    def addVerbosePacket(self, packet):
        self.packetsVerbose.append(packet)



authData = AlexaPacketTrackingData()

#########
# Intents
#########

@ask.launch
def launch():
    welcome_text = render_template('welcome')
    return question(welcome_text)

@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = render_template('help')
    return statement(help_text).simple_card('Hilfe', help_text)

@ask.intent('AMAZON.StopIntent')
def stop():
    global authData
    authData = None
    stop_text = render_template('stop')
    return statement(stop_text)

@ask.intent('AMAZON.CancelIntent')
def cancel():
    global authData
    authData = None
    stop_text = render_template('stop')
    return statement(stop_text)

@ask.intent('LoginIntent')
def login():
    global authData
    if authData.sessionId:
        return question('')
    authData = AlexaPacketTrackingData(email='alexa_test@itestra.de', password='testtest')
    authenticate()
    if authData.sessionId:
        fetchPacketIds()
        fetchDataAsync()
        login_success_text = render_template('login_success', email=authData.email)
        return question(login_success_text)
    else:
        error_text = render_template('error')
        return statement(error_text)

@ask.intent('PaketNumberIntent')
def packet_number():
    if not authData.packetIds:
        return noPacketsRegistratedQuestion()
    number_of_packets_text = render_template('number_of_packets', number=len(authData.packetIds))
    return question(number_of_packets_text)

@ask.intent('OverviewIntent')
def overview():
    if not authData.packetIds:
        return noPacketsRegistratedQuestion()
    overviewDict = dict()
    for packetInfo in authData.packetsVerbose:
        if not (packetInfo['sender_name'], packetInfo['receiver_name']) in overviewDict:
            overviewDict[(packetInfo['sender_name'], packetInfo['receiver_name'])] = [packetInfo]
        else:
            overviewDict[(packetInfo['sender_name'], packetInfo['receiver_name'])].append(packetInfo)
    overviewMessages = list()
    overviewDictList = list(overviewDict)
    for senderReceiverTuple in overviewDictList:
        template_name = 'there_are_x_packets'
        if senderReceiverTuple == overviewDictList[0]:
            template_name += '_0'
        elif senderReceiverTuple == overviewDictList[-1]:
            template_name += '_2'
        else:
            template_name += '_1'
        overviewMessages.append(render_template(template_name, 
            number=len(overviewDict[senderReceiverTuple]),
            sender=senderReceiverTuple[0],
            receiver=senderReceiverTuple[1]))
    return question(' '.join(overviewMessages))

@ask.intent('PersonPaketIntent')
def personPaketInfo(name):
    logging.debug("Got name: ", name)
    if not authData.packetIds:
        return noPacketsRegistratedQuestion()
    if not name:
        get_name_text = render_template('get_name')
        return question(get_name_text)
    personPacketInfoMessages = list()
    for packetInfo in authData.packetsVerbose:
        if not name.lower() in packetInfo['sender_name'].lower() and not name.lower() in packetInfo['receiver_name'].lower():
            continue
        template_name = ''
        current_city = ''
        if 'deliveryTime' in packetInfo:
            template_name = 'already_delivered'
        elif not packetInfo['stations']:
            template_name = 'just_sent'
        else:
            template_name = 'packet_on_the_way'
            current_city = packetInfo['stations'][-1]['location']
        personPacketInfoMessages.append(render_template(template_name,
            city = current_city,
            sender = packetInfo['sender_name'],
            receiver = packetInfo['receiver_name']))
    if personPacketInfoMessages:
        return question(' '.join(personPacketInfoMessages))
    else:
        no_paket_text = render_template('no_paket', name=name)
        return question(no_paket_text)
        

########
# Filter
########

@app.template_filter()
def speakable_number(number):
    if number == 1:
        return render_template('speakable_one')
    return number

@app.template_filter()
def get_plural_e(number):
    if number != 1:
        return 'e'
    return ''

@app.template_filter()
def get_plural_n(number):
    if number != 1:
        return 'n'
    return ''


#########
# Helper
#########

def noPacketsRegistratedQuestion():
    no_paket_registered_text = render_template('no_paket_registered')
    return question(no_paket_registered_text)

def fetchDataAsync():
    fetchPacketDataThread = threading.Thread(target=fetchPacketData)
    fetchPacketDataThread.start()

def fetchPacketData():
    for packetId in authData.packetIds:
        request = urllib.request.Request(TRACKING_BASE_URL + '/packetStatus/' + packetId)
        response = urllib.request.urlopen(request)
        responseJson = json.loads(response.read().decode('utf8'))
        authData.addVerbosePacket(responseJson)

def fetchPacketIds():
    request = urllib.request.Request(USER_BASE_URL + '/get_packets_from_user/' + authData.sessionId)
    response = urllib.request.urlopen(request)
    responseJson = json.loads(response.read().decode('utf8'))
    authData.setPacketIds(responseJson['packets'])

def authenticate():
    request = urllib.request.Request(USER_BASE_URL + '/authenticate_user',
        data = json.dumps({"email":authData.email, "password":authData.password}).encode('utf8'),
        headers = {"Content-Type":"application/json"})
    response = urllib.request.urlopen(request)
    responseJson = json.loads(response.read().decode('utf8'))
    authData.sessionId = responseJson['session_id']

if __name__ == '__main__':
    app.run()
    # authData = AlexaPacketTrackingData(email='alexa_test@itestra.de', password='testtest')
    # authenticate()
    # fetchPacketIds()
    # print(authData.packetIds)
