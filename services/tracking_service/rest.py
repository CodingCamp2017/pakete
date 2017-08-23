#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, abort, Response
from tracking_service import TrackingService
import mykafka
from Exceptions import InvalidActionException, CommandFailedException
import json
import sys

app = Flask(__name__)
tracking_service = TrackingService(mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'package'))

@app.route('/', methods=['GET'])
def restRoot():
    # TODO testing only, remove
    responsestr = tracking_service.read_packages()
    code = 200
    response = Response(response=responsestr, status=code, mimetype="text/plain")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/packageStatus/<id>', methods=['GET'])
def restPackageStatus(id):
    if id is None:
        return "No ID specified."
    
    return tracking_service.package_status(id)


if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(debug=True, host='0.0.0.0', port=port) 
