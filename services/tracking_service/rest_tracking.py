#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

from flask import Flask
from tracking_service import TrackingService

sys.path.append(os.path.relpath('../rest_common'))
sys.path.append(os.path.relpath('../mykafka'))
import rest_common
import mykafka


app = Flask(__name__)#Initialize flask
# Create the TrackingService
tracking_service = TrackingService(mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'packet'))

'''
This function is called whenever a client visits the root "page" on
this server.
'''
@app.route('/', methods=['GET'])
def restRoot():    
    return rest_common.create_error_response(404, "No ID specified.")

'''
This function is called whenever a client visits the '/packetStatus' "page" on
this server.
'''
@app.route('/packetStatus/<packetId>', methods=['GET'])
def restPackageStatus(packetId):
    if packetId is None:
        return rest_common.create_error_response(404, "No ID specified.")
    
    res = tracking_service.packetStatus(packetId)
    if res is None:
        return rest_common.create_error_response(404, "Package not found")
        
    return rest_common.create_response(200, res)

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(debug=True, host='0.0.0.0', port=port) 
