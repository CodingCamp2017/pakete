#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, abort, Response
from tracking_service import TrackingService
import mykafka
from Exceptions import InvalidActionException, CommandFailedException
import json
import sys

app = Flask(__name__)
tracking_service = TrackingService(mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'packet'))

def createResponse(code, jsonobj):
    string = json.dumps(jsonobj)
    response = Response(response=string, status=code, mimetype="application/json")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/', methods=['GET'])
def restRoot():    
    createResponse(404, "No ID specified.")

@app.route('/packetStatus/<id>', methods=['GET'])
def restPackageStatus(id):
    if id is None:
        return "No ID specified."
    
    res = tracking_service.packetStatus(id)
    if res is None:
        createResponse(404, "Package not found")
        return
        
    return createResponse(200, res)

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(debug=True, host='0.0.0.0', port=port) 
