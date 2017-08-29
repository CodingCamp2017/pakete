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

TRACKING_BASE_URL = 'http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8001'
USER_BASE_URL = 'http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8002'

app = Flask(__name__)
ask = Ask(app, '/')

class AlexaPacketTrackingData:
    def __init__(self, email='', password=''):
        self.email = email
        self.password = password
        self.sessionId = ''
        self.packetIds = list()
        self.packetsVerbose = list()

    def setSessionId(sessionId):
        self.sessionId = sessionId

    def setPacketIds(packetIds):
        self.packetIds = packetIds

    def addVerbosePacket(id, packet):
        self.packetsVerbose.append(packet)



authData = AlexaPacketTrackingData(email='test@test.de', password='testtest')

#########
# Intents
#########

@ask.launch
def launch():
    welcome_text = render_template('welcome')
    help_text = render_template('help')
    return question(welcome_text)

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

@ask.intent('LoginIntent')
def login():
    authenticate()
    if authData.sessionId:
        login_success_text = render_template('login_success')
        return question(login_success_text)
    else:
        error_text = render_template('error')
        return statement(error_text)

@ask.intent('PaketNumberIntent')
def packet_number():
    fetchPacketIds()
    number_of_packets_text = render_template('number_of_packets', number=len(packetIds))
    return question(number_of_packets_text)

@ask.intent('OverviewIntent')
def overview():
    fetchPacketData()
    overviewDict = dict()
    for packetInfo in authData.packetsVerbose:
        if not (packetInfo['sender_name'], packetInfo['receiver_name']) in overviewDict:
            overviewDict[(packetInfo['sender_name'], packetInfo['receiver_name'])] = [packetInfo]
        else:
            overviewDict[(packetInfo['sender_name'], packetInfo['receiver_name'])].append(packetInfo)

    overviewMessages = list()
    for senderReceiverTuple in overviewDict:
        overviewMessages.append(render_template('there_are_x_packets', 
            number=len(overviewDict[senderReceiverTuple])),
            sender=senderReceiverTuple[0],
            receiver=senderReceiverTuple[1])

    return question('...'.join(overviewMessages))

########
# Filter
########

@app.template_filter()
def speakable_number(number):
    if number == 1:
        return render_template('speakable_one')
    return number

@app.template_filter()
def plural_e(number):
    if number != 1:
        return 'e'
    return ''

@app.template_filter()
def plural_n(number):
    if number != 1:
        return 'n'
    return ''


#########
# Helper
#########

def fetchPacketData():
    for packetId in authData.packetIds:
        request = urllib.request.Request(TRACKING_BASE_URL + '/packetStatus/' + packet_number)
        response = urllib.request.urlopen(request)
        responseJson = json.loads(json.loads(response.read().decode('utf8')))
        authData.addVerbosePacket(packetId, responseJson)

# def get_packet_info(packet_number):
#     if packet_number > len(packets):
#         return None
#     packet_number = packets[packet_number-1]
#     request = urllib.request.Request(TRACKING_BASE_URL + '/packetStatus/' + packet_number)
#     response = urllib.request.urlopen(request)
#     responseJson = json.loads(response.read().decode('utf8'))
#     return responseJson

def fetchPacketIds():
    authData.setPacketIds(packets)

def authenticate():
    pass
    #createNewUser()
    session = None# session

if __name__ == '__main__':
    app.run()