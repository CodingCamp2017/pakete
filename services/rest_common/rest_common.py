from Exceptions import InvalidActionException
import Exceptions
import json
from flask import Response


def get_rest_data(response):
    if response.json != None:
        return response.json
    elif response.form != None:
        return response.form
    raise InvalidActionException(Exceptions.TYPE_NO_DATA_FOUND, None, "Didn't find parameter data, required either json or form data")
    
def create_response(code, data = {}):
    string = json.dumps(data)
    response = Response(response=string, status=code, mimetype="application/json")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

def create_error_response(errcode, message):
    return create_response(errcode, {"error":str(message)})