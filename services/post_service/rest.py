#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, abort
from post_service import register, updateLocation, delivered
from Exceptions import InvalidActionException, CommandFailedException

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def restRegister():
    try:
    	return register(request.json)
    except (CommandFailedException, InvalidActionException) as e:
        return e.message

@app.route('/updateLocation', methods=['POST'])
def restUpdateLocation():
    try:
    	return updateLocation(request.json)
    except (CommandFailedException, InvalidActionException) as e:
        return e.message
    
@app.route('/delivered', methods=['POST'])
def restDelivered():
    try:
    	return delivered(request.json)
    except (CommandFailedException, InvalidActionException) as e:
        return e.message
    
if __name__ == '__main__':
    app.run(debug=True)