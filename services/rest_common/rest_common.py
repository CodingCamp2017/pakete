import os
import sys
sys.path.append(os.path.relpath('../common'))
import Exceptions
import json
from flask import Response

'''
Returns a dictionary containing the payload data of the given flask.Response.
Accepted payload data is form data or json.
Raises Exceptions.InvalidActionException if no data could be extracted
'''
def get_rest_data(response):
    if response.json != None:
        return response.json
    elif response.form != None:
        return response.form
    raise Exceptions.InvalidActionException(Exceptions.TYPE_NO_DATA_FOUND, None, "Didn't find parameter data, required either json or form data")

'''
Creates and returns a flask.Response with the given HTTP status code.
data (optional): a dictionary containing data to send back
'''
def create_response(code, data = {}):
    string = json.dumps(data)
    response = Response(response=string, status=code, mimetype="application/json")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

'''
Creates and returns a flask.Response with the given HTTP status code.
message: exception or string will be sent back
'''
def create_error_response(errcode, message):
    return create_response(errcode, {"error":str(message)})

def create_cookie_response(code, session_id):
    response = Response(status=code)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.set_cookie('session_id', bytes(session_id, 'utf-8'))
    return response