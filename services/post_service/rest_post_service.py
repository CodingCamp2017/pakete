#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import getopt
from flask import Flask, request
from post_service import PostService
import mykafka
from Exceptions import InvalidActionException, CommandFailedException

sys.path.append(os.path.relpath('../rest_common'))
import rest_common

app = Flask(__name__)
post_service = PostService(mykafka.create_producer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092))
    
    

@app.route('/register', methods=['POST'])
def restRegister():
    try:
        data = rest_common.get_rest_data(request)
        packet_id = post_service.register_package(data)
        return rest_common.create_response(200, {"id":str(packet_id)})
    except InvalidActionException as e:
        return rest_common.create_error_response(400, e)
    except CommandFailedException as e:
        return rest_common.create_error_response(504, e)

@app.route('/updateLocation', methods=['POST'])
def restUpdateLocation():
    try:
        data = rest_common.get_rest_data(request)
        post_service.update_package_location(data)
        return rest_common.create_response(200)
    except InvalidActionException as e:
        return rest_common.create_error_response(400, e)
    except CommandFailedException as e:
        return rest_common.create_error_response(504, e)
    
@app.route('/delivered', methods=['POST'])
def restDelivered():
    try:
        data = rest_common.get_rest_data(request)
        post_service.mark_delivered(data)
        return rest_common.create_response(200)
    except InvalidActionException as e:
        return rest_common.create_error_response(400, e)
    except CommandFailedException as e:
        return rest_common.create_error_response(504, e)
        
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