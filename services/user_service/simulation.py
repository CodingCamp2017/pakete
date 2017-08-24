
from user_service import UserService
from random import randint, sample
import string

import codecs
import json
import sys
import os
sys.path.append(os.path.relpath('../mykafka'))
sys.path.append(os.path.relpath('../common'))
import mykafka
import signal
import threading
import time
import uuid

from Exceptions import UserExistsException, UserUnknownException, InvalidSessionIdException, SessionElapsedException, InvalidPasswortException


char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
sizes = ['small','normal','big']
fakedata = json.load(codecs.open('fakedata.json', 'r', 'utf-8-sig'))['data']
user_service = UserService(mykafka.create_producer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092))


def create_test_add_user_json():
    user = fakedata[randint(0, len(fakedata)-1)]
    
    data = {'email' : user['name'].replace(' ','.').replace('-', '_')+'@mail.de',
            'name' : user['name'],
            'street' : user['name'],
            'zip' : str(randint(10000,99999)),
            'city' : user['name'],
            'password' : ''.join(sample(char_set*8, 8))}
    return json.dumps(data)

def create_simple_test_user():
    return {'email' : 'bal@as.de', 'password' : 'shdjfhfh'}


def create_add_packet_data(email, session_id):
    return {'email' : email,
            'packet' : str(uuid.uuid1()),
            'session_id' : session_id}
        
def create_session_data(email, session_id):
    return {'email' : email,
            'session_id' : session_id}


def simulate_user_behaviour():
    for i in range(3):
        user_data = create_simple_test_user()
        email = user_data['email']
        user_service.add_user(user_data)
        print('User {} added'.format(user_data['email']))
        #time.sleep(randint(1,2))
        
        for i in range(randint(0,10)):
            
            session_id = user_service.authenticate_user(user_data)
            print('User {} authenticated '.format(user_data['email']))
            #time.sleep(randint(1,2))
            for j in range(randint(0,10)):
                if randint(0,1):
                    user_service.add_packet(create_add_packet_data(email, session_id))
                    print('User {} added packet'.format(user_data['email']))
                else:
                    packets = user_service.get_packets_from_user(create_session_data(email, session_id))
                    print('User {} has packets {}'.format(user_data['email']), packets)
                #time.sleep(randint(1,2))
            user_service.logout_user(create_session_data(user_data['email'], session_id))
            print('User {} logged out'.format(user_data['email']))
            #time.sleep(randint(1,2))
    
        #session_id = user_service.authenticate_user(user_data)
        #print('User {} authenticated with session id {}'.format(user_data['email']), session_id)
        #time.sleep(randint(1,2))
        #user_service.delete(create_session_data(user_data['email'], session_id))
        #print('User {} deleted'.format(user_data['email']), session_id)
        #time.sleep(randint(1,2))


if __name__ == '__main__':
    simulate_user_behaviour()
