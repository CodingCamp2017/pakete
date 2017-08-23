#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import getopt
from flask import Flask, request, abort, jsonify, make_response, Response
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
    
def createResponse(code, jsonobj):
    string = json.dumps(jsonobj)
    response = Response(response=string, status=code, mimetype="application/json")
    response.headers["Access-Control-Allow-Origin"] = "*"
    #response.headers["Content-Type"] = "
    return response

@app.route('/register', methods=['POST'])
def restRegister():
    try:
        data = getData(request)
        packet_id = post_service.register_package(data)
        return createResponse(200, {"id":str(packet_id)})
    except InvalidActionException as e:
        abort(400, e)
    except CommandFailedException as e:
        abort(504, e)

@app.route('/updateLocation', methods=['POST'])
def restUpdateLocation():
    try:
        data = getData(request)
        post_service.update_package_location(data)
        return createResponse(200, {})
    except InvalidActionException as e:
        abort(400, e)
    except CommandFailedException as e:
        abort(504, e)
    
@app.route('/delivered', methods=['POST'])
def restDelivered():
    try:
        data = getData(request)
        post_service.mark_delivered(data)
        return createResponse(200, {})
    except InvalidActionException as e:
        abort(400, e)
    except CommandFailedException as e:
        abort(504, e)
        
def print_help():
    print("Options:\n\t-p Port to use")
    
if __name__ == '__main__':
    port = 0
    try:
        options, args = getopt.getopt(sys.argv[1:], "p:")
    except getopt.GetoptError:
        print_help()
        sys.exit(1)
    for opt, arg in options:
        if(opt == "-p"):
            try:
                port = int(arg)
            except ValueError:
                print("Cannot parse port: "+arg)
                sys.exit(1)
        else:
            print("Unknown option "+opt)
            sys.exit(1)
    app.run(debug=True, port=port, host="0.0.0.0")