#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

from flask import Flask
from tracking_service import TrackingService

sys.path.append(os.path.relpath('../common'))
sys.path.append(os.path.relpath('../rest_common'))
sys.path.append(os.path.relpath('../mykafka'))
import rest_common
import mykafka
import packet_regex
from Exceptions import InvalidActionException, TYPE_INVALID_KEY


app = Flask(__name__)#Initialize flask
# Create the TrackingService
tracking_service = TrackingService(mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'packet'))


'''
Returns a http response with error code 404 and json data describing the problem
with invalid value.
'''
def create_invalid_key_error(value = ""):
    return rest_common.create_response(404, InvalidActionException(TYPE_INVALID_KEY, "packet_id", "Invalid value: "+value+" for key packet_id").toDict())

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

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(debug=True, host='0.0.0.0', port=port) 
