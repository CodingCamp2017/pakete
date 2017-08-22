#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, abort
from tracking_service import TrackingService
import mykafka
from Exceptions import InvalidActionException, CommandFailedException
import json

app = Flask(__name__)
tracking_service = TrackingService(mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'package'))

@app.route('/', methods=['GET'])
def restRoot():
    response = tracking_service.read_packages()
    return "Test: " + response

@app.route('/packageStatus', methods=['GET'])
def restPackageStatus():
    id = request.args.get('id')
    
    if id is None:
        return "ID not specified"
    
    return json.dumps(tracking_service.package_status(id))


if __name__ == '__main__':
    app.run(debug=True) 