#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, abort, jsonify, make_response
from post_service import PostService
import mykafka
from Exceptions import InvalidActionException, CommandFailedException

app = Flask(__name__)
post_service = PostService(mykafka.create_producer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092))

def getData(response):
    if response.json != None:
        return response.json
    elif response.form != None:
        return response.form
    raise InvalidActionException("Didn't find parameter data, required either json or form data")

@app.route('/register', methods=['POST'])
def restRegister():
    try:
        data = getData(request)
        packet_id = post_service.register_package(data)
        return jsonify({"id":packet_id})
    except InvalidActionException as e:
        abort(400, e)
    except CommandFailedException as e:
        abort(504, e)

@app.route('/updateLocation', methods=['POST'])
def restUpdateLocation():
    try:
        data = getData(request)
        post_service.update_package_location(data)
        return make_response(jsonify({}), 200)
    except InvalidActionException as e:
        abort(400, e)
    except CommandFailedException as e:
        abort(504, e)
    
@app.route('/delivered', methods=['POST'])
def restDelivered():
    try:
        data = getData(request)
        post_service.mark_delivered(data)
        return make_response(jsonify({}), 200)
    except InvalidActionException as e:
        abort(400, e)
    except CommandFailedException as e:
        abort(504, e)
    
if __name__ == '__main__':
    app.run(debug=True)