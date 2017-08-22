#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, abort
from post_service import PostService
import mykafka
from Exceptions import InvalidActionException, CommandFailedException

app = Flask(__name__)
post_service = PostService(mykafka.create_producer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092))

@app.route('/register', methods=['POST'])
def restRegister():
    try:
    	return post_service.register_package(request.json)
    except (CommandFailedException, InvalidActionException) as e:
        return e.message

@app.route('/updateLocation', methods=['POST'])
def restUpdateLocation():
    try:
    	return post_service.update_package_location(request.json)
    except (CommandFailedException, InvalidActionException) as e:
        return e.message
    
@app.route('/delivered', methods=['POST'])
def restDelivered():
    try:
    	return post_service.mark_delivered(request.json)
    except (CommandFailedException, InvalidActionException) as e:
        return e.message
    
if __name__ == '__main__':
    app.run(debug=True)