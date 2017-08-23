#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

from flask import Flask, request, abort, Response
from tracking_service import TrackingService

sys.path.append(os.path.relpath('../rest_common'))
import rest_common

import mykafka

from Exceptions import InvalidActionException, CommandFailedException


app = Flask(__name__)
tracking_service = TrackingService(mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'packet'))

@app.route('/', methods=['GET'])
def restRoot():    
    rest_common.create_error_response(404, "No ID specified.")

@app.route('/packetStatus/<id>', methods=['GET'])
def restPackageStatus(id):
    if id is None:
        return "No ID specified."
    
    res = tracking_service.packetStatus(id)
    if res is None:
        rest_common.create_error_response(404, "Package not found")
        return
        
    return rest_common.create_response(200, res)

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(debug=True, host='0.0.0.0', port=port) 
