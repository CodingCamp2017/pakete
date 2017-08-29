#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import eventlet
eventlet.monkey_patch()#make pythons threads greenlets


import sys
import os

from flask import Flask, request
from flask_socketio import SocketIO
from tracking_service import TrackingService
from client_subscriptions import ClientSubscriptionManager

sys.path.append(os.path.relpath('../common'))
sys.path.append(os.path.relpath('../rest_common'))
sys.path.append(os.path.relpath('../mykafka'))
import rest_common
import mykafka
import packet_regex
from Exceptions import InvalidActionException, TYPE_INVALID_KEY, TYPE_NO_DATA_FOUND, TYPE_KEY_NOT_FOUND




app = Flask(__name__)#Initialize flask
socketio = SocketIO(app)
# Create the TrackingService
clients = ClientSubscriptionManager()

def client_update_location(packet_id, time, location, vehicle):
    sids = clients.get_subscribed_clients_for_id(packet_id)
    if sids:
        data = {'packet_id':packet_id, 'time':time, 'location':location, 'vehicle':vehicle}
        for sid in sids:
            socketio.emit('update', data, namespace='/packetStatus', room=sid)
            
def client_delivered(packet_id, time):
    sids = clients.get_subscribed_clients_for_id(packet_id)
    if sids:
        data = {'packet_id':packet_id, 'deliveryTime':time}
        for sid in sids:
            socketio.emit('update', data, namespace='/packetStatus', room=sid)

tracking_service = TrackingService(mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'packet'), client_update_location, client_delivered)


'''
Returns a http response with error code 404 and json data describing the problem
with invalid value.
'''
def create_invalid_key_error(value = ""):
    return rest_common.create_response(404, InvalidActionException(TYPE_INVALID_KEY, "packet_id", "Invalid value: "+value+" for key packet_id").toDict())

def send_invalid_action_error(sid, event, namespace, error_type, message, key=None):
    errJson = InvalidActionException(error_type, key, message).toDict()
    socketio.emit(event, errJson, namespace=namespace, room=sid)
    
def send_invalid_key_error(sid, event, namespace, key):
    send_invalid_action_error(sid, event, namespace, TYPE_INVALID_KEY, "Invalid value for key", key)

'''
This function is called whenever a client visits the '/packetStatus' "page" on
this server.
'''
@app.route('/packetStatus/<packetId>', methods=['GET'])
def restPacketStatus(packetId):
    if not packet_regex.regex_matches_exactly(packet_regex.regex_id, packetId):
        return create_invalid_key_error(packetId)
        
    res = tracking_service.packetStatus(packetId)
    if res is None:
        return rest_common.create_error_response(404, "Packet not found")
    else:
        return rest_common.create_response(200, res)

@app.route('/packetStatus/', methods=['GET'])
def invalidPacketId():
    return create_invalid_key_error()

@socketio.on('connect', namespace='/packetStatus')
def client_connected():
    clients.client_connected(request.sid)
    
@socketio.on('disconnect', namespace='/packetStatus')
def client_disconnected():
    clients.client_disconnect(request.sid)

@socketio.on('subscribe', namespace='/packetStatus')
def client_subscribed(message):
    if not message:
        send_invalid_action_error(request.sid, 'subscribe', '/packetStatus', TYPE_NO_DATA_FOUND, "No json data received")
        return
    if not "packet_id" in message:
        send_invalid_action_error(request.sid, 'subscribe', '/packetStatus', TYPE_KEY_NOT_FOUND, "Didn't find key packet_id", "packet_id")
        return
    packet_id = message["packet_id"]
    if not packet_regex.regex_matches_exactly(packet_regex.regex_id, packet_id):
        send_invalid_key_error(request.sid, 'subscribe', '/packetStatus', "packet_id")
        return
    clients.client_subscribe(request.sid, packet_id)

        
        
if __name__ == '__main__':
    port = int(sys.argv[1])
    socketio.run(app, debug=True, host='0.0.0.0', port=port)
