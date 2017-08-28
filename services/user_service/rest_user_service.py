#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.relpath('../mykafka'))
sys.path.append(os.path.relpath('../rest_common'))
import rest_common

import getopt
from Exceptions import InvalidActionException, UserExistsException, UserUnknownException, SessionElapsedException, InvalidPasswortException, PacketNotFoundException, NoPacketException, NoSessionIdException
from flask import Flask, request, session
from datetime import timedelta
from user_service import UserService
import signal


app = Flask(__name__)
app.secret_key = "hallo blub foo bar"
app.config['SESSION_TYPE'] = 'filesystem'

user_service = UserService()

def sigint_handler(signum, frame):
    print("Interrupted")
    user_service.close()

signal.signal(signal.SIGINT, sigint_handler)


@app.before_request
def make_session_permanent():
    pass
    #session.permanent = True
    #app.permanent_session_lifetime = timedelta(minutes=5)

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
        userEmail = data['email']
        if(user_service.authenticate_user(data)) :
            print("Session with user " + userEmail)
            session['userEmail'] = userEmail
            session.modified = True;
            
            print('SESSION: ' + str(session))

            return rest_common.create_response(200)
    except InvalidActionException as e:
        return rest_common.create_error_response(400, e)
    except UserUnknownException as e:
        return rest_common.create_error_response(404, e)
    except InvalidPasswortException as e:
        return rest_common.create_error_response(401, e)
    except TypeError as e:
        print("TypeError in authenticate_user")
        return "123"
    
@app.route('/update_user_adress', methods=['POST'])
def restUpdateAdress():
    try:
        data = rest_common.get_rest_data(request)
        user_service.update_user_adress(data)
        return rest_common.create_response(200)
    except InvalidActionException as e:
        return rest_common.create_error_response(400, e)
    except UserUnknownException as e:
        return rest_common.create_error_response(404, e)
    except SessionElapsedException as e:
        return rest_common.create_error_response(401, e)

@app.route('/add_packet_to_user', methods=['POST'])
def restAddPacket():
    try:
        packet_id = request.json('packet')
        #return rest_common.create_error_response(421, str(packet_id))
        if not packet_id:
            raise NoPacketException
        session_id = request.cookies.get('session_id')
        if not packet_id:
            raise NoSessionIdException
        data = {'packet' : packet_id, 'session_id' : session_id}
        user_service.add_packet_to_user(data)
        return rest_common.create_response(200)
    except NoPacketException as e:
        return rest_common.create_error_response(421, e)
    except NoSessionIdException as e:
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
    print('__________SESSION: ' + str(session))

    try:
        if 'userEmail' in session:
            userEmail = session['userEmail'];
            print("Logged in as " + str(userEmail))
            packets = user_service.get_packets_from_user(userEmail)
        else:
            print("Not logged in")
            return rest_common.create_error_response(400, "User not logged in.") # TODO which error code?
        return rest_common.create_response(200, packets)
    except InvalidActionException as e:
        return rest_common.create_error_response(400, e)
    except SessionElapsedException as e:
        return rest_common.create_error_response(401, e)
    except UserUnknownException as e:
        return rest_common.create_error_response(404, e)
    except NoSessionIdException as e:
        return rest_common.create_error_response(422, e)
    
@app.route('/delete_user', methods=['POST'])
def restDeleteUser():
    try:
        session_id = request.cookies.get('session_id')
        user_service.delete_user(session_id)
        return rest_common.create_response(200)
    except InvalidActionException as e:
        return rest_common.create_error_response(400, e)
    except UserUnknownException as e:
        return rest_common.create_error_response(404, e)
    except SessionElapsedException as e:
        return rest_common.create_error_response(401, e)
    
        
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