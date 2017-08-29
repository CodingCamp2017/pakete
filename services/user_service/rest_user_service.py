#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.relpath('../mykafka'))
sys.path.append(os.path.relpath('../rest_common'))
import rest_common

import getopt
from Exceptions import InvalidActionException, UserExistsException, UserUnknownException, SessionElapsedException, InvalidPasswortException, PacketNotFoundException, NoPacketException, InvalidSessionIdException, NoSessionIdException
from flask import Flask, request
from user_service import UserService


app = Flask(__name__)
app.secret_key = "hallo blub foo bar"
app.config['SESSION_TYPE'] = 'filesystem'

user_service = UserService()


@app.route('/add_user', methods=['POST'])
def restAddUser():
    try:
        data = rest_common.get_rest_data(request)
        user_service.add_user(data)
        return rest_common.create_response(200)
    except InvalidActionException as e:
        return rest_common.create_error_response(400, e)
    except UserExistsException as e:
        return rest_common.create_error_response(409, e)
        
@app.route('/authenticate_user', methods=['POST'])
def restAuthenticateUser():
    try:
        data = rest_common.get_rest_data(request)
        session_id = user_service.authenticate_user(data)
        return rest_common.create_response(200, {'session_id':str(session_id)})
    except InvalidActionException as e:
        return rest_common.create_error_response(400, e)
    except UserUnknownException as e:
        return rest_common.create_error_response(404, e)
    except InvalidPasswortException as e:
        return rest_common.create_error_response(401, e)
    except TypeError as e:
        print("TypeError in authenticate_user")
        return "123"
    
#@app.route('/update_user_adress', methods=['POST'])
#def restUpdateAdress():
#    try:
#        data = rest_common.get_rest_data(request)
#        user_service.update_user_adress(data)
#        return rest_common.create_response(200)
#    except InvalidActionException as e:
#        return rest_common.create_error_response(400, e)
#    except UserUnknownException as e:
#        return rest_common.create_error_response(404, e)
#    except SessionElapsedException as e:
#        return rest_common.create_error_response(401, e)

@app.route('/add_packet_to_user', methods=['POST'])
def restAddPacket():
    try:
        data  =rest_common.get_rest_data(request)
        user_service.add_packet_to_user(data)
        return rest_common.create_response(200)
    except NoPacketException as e:
        return rest_common.create_error_response(421, e)
    except (InvalidSessionIdException, NoSessionIdException) as e:
        return rest_common.create_error_response(422, e)
    except InvalidActionException as e:
        return rest_common.create_error_response(400, e)
    except UserUnknownException as e:
        return rest_common.create_error_response(404, e)
    except SessionElapsedException as e:
        return rest_common.create_error_response(401, e)
    except PacketNotFoundException as e:
        return rest_common.create_error_response(410, e)
    
@app.route('/get_packets_from_user', methods=['GET'])
def restGetPacket():
    try:
        data = rest_common.get_rest_data(request)
        packets = user_service.get_packets_from_user(data)
        if not packets:
            raise NoPacketException
        return rest_common.create_response(200, packets)
    except InvalidActionException as e:
        return rest_common.create_error_response(400, e)
    except SessionElapsedException as e:
        return rest_common.create_error_response(401, e)
    except UserUnknownException as e:
        return rest_common.create_error_response(404, e)
    except (InvalidSessionIdException, NoSessionIdException) as e:
        return rest_common.create_error_response(422, e)
    
@app.route('/delete_user', methods=['POST'])
def restDeleteUser():
    try:
        data = rest_common.get_rest_data(request)
        user_service.delete_user(data)
        return rest_common.create_response(200)
    except InvalidActionException as e:
        return rest_common.create_error_response(400, e)
    except UserUnknownException as e:
        return rest_common.create_error_response(404, e)
    except SessionElapsedException as e:
        return rest_common.create_error_response(401, e)
    except (InvalidSessionIdException, NoSessionIdException) as e:
        return rest_common.create_error_response(422, e)
    
@app.route('/logout', methods=['POST'])
def restLogoutUser():
    try:
        data = rest_common.get_rest_data(request)
        user_service.logout_user(data)
        return rest_common.create_response(200)
    except InvalidActionException as e:
        return rest_common.create_error_response(400, e)
    except UserUnknownException as e:
        return rest_common.create_error_response(404, e)
    except SessionElapsedException as e:
        return rest_common.create_error_response(401, e)
    except (InvalidSessionIdException, NoSessionIdException) as e:
        return rest_common.create_error_response(422, e)
    
        
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