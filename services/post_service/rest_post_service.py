
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import getopt
from flask import Flask, request
from post_service import PostService
import mykafka

sys.path.append(os.path.relpath('../rest_common'))
sys.path.append(os.path.relpath('../common'))
import rest_common
import Exceptions

app = Flask(__name__)# Initializes Flask as web interface
# start the PostService
post_service = PostService(mykafka.create_producer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092))
    
'''
Copies a dictionary and returns the copy
'''
def copy_dict(d):
    return { key : value for (key, value) in d.items()}

'''
This function is called whenever a client visits the '/register' "page" on
this server.
'''
@app.route('/register', methods=['POST'])
def restRegister():
    try:
        request_data = rest_common.get_rest_data(request)
        data = copy_dict(request_data)
        if 'auto_deliver' not in data:
            data['auto_deliver'] = False
        elif not isinstance(data['auto_deliver'], bool):
            if isinstance(data['auto_deliver'], str) and data['auto_deliver'].lower() == 'true':
                data['auto_deliver'] = True
            elif isinstance(data['auto_deliver'], str) and data['auto_deliver'].lower() == 'false':
                data['auto_deliver'] = False
            else:
                err_msg = 'Invalid value for auto_deliver flag! Type is ' + str(type(data['auto_deliver'])) + ', value is ' + str(data['auto_deliver'])
                print(err_msg)
                return rest_common.create_error_response(400, err_msg)
        packet_id = post_service.register_packet(data)
        return rest_common.create_response(200, {"packet_id":str(packet_id)})
    except Exceptions.InvalidActionException as e:
        return rest_common.create_response(400, e.toDict())
    except Exceptions.CommandFailedException as e:
        return rest_common.create_error_response(504, e)

'''
This function is called whenever a client visits the '/packet/packet_id/update
"page" on this server, where packet_id is the id of the packet the client wants
to update
'''
@app.route('/packet/<packet_id>/update', methods=['POST'])
def restUpdateLocation(packet_id):
    try:
        request_data = rest_common.get_rest_data(request)
        #print(str(request_data))
        data = copy_dict(request_data)#Copy the dict as request_data is immutable
        data["packet_id"] = packet_id
        #print(str(data))
        post_service.update_packet_location(data)
        return rest_common.create_response(200)
    except Exceptions.InvalidActionException as e:
        print("InvalidAction: update for packet_id '"+packet_id+"' failed: "+str(e))
        return rest_common.create_response(400, e.toDict())
    except Exceptions.CommandFailedException as e:
        print("CommandFailed: update for packet_id '"+packet_id+"' failed: "+str(e))
        return rest_common.create_error_response(504, e)
    
'''
This function is called whenever a client visits the '/packet/packet_id/delivered
"page" on this server, where packet_id is the id of the packet the client wants
to be marked as delivered
'''
@app.route('/packet/<packet_id>/delivered', methods=['POST'])
def restDelivered(packet_id):
    try:
        request_data = rest_common.get_rest_data(request)
        data = copy_dict(request_data)
        data["packet_id"] = packet_id
        post_service.mark_delivered(data)
        return rest_common.create_response(200)
    except Exceptions.InvalidActionException as e:
        print("InvalidAction: register for packet_id '"+packet_id+"' failed: "+str(e))
        return rest_common.create_response(400, e.toDict())
    except Exceptions.CommandFailedException as e:
        print("CommandFailed: register for packet_id '"+packet_id+"' failed: "+str(e))
        return rest_common.create_error_response(504, e)

'''
Prints options for starting the server
'''
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