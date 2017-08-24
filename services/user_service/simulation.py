
from user_service import UserService
from random import randint, sample
import string

import codecs
import json
import sys
import os
sys.path.append(os.path.relpath('../mykafka'))
import mykafka
import signal
import threading
import time
import uuid

from Exceptions import UserExistsException, UserUnknownException, InvalidSessionIdException, SessionElapsedException, InvalidPasswortException

def sigint_handler(signum, frame):
    print("Interrupted")
    threadStop.set()

lock = threading.Lock()
threadStop = threading.Event()
signal.signal(signal.SIGINT, sigint_handler)


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

def create_authentification_data(user_data):
    user = json.loads(user_data)
    return json.dumps({'email' : user['email'], 'password' : user['password']})

def create_add_packet_data(email, session_id):
    user = json.loads(user_data)
    return json.dumps({'email' : user['email'],
                       'packet' : str(uuid.uuid1()),
                       'password' : user['password']})
        
def create_session_data(email, session_id):
    user = json.loads(user_data)
    return json.dumps({'email' : user['email'],
                       'password' : user['password']})

user_options = {0 : user_service.add_packet_to_user,
                1 : user_service.get_packets_from_user}

user_data = {0 : create_add_packet_data,
             1 : create_session_data}

def simulate_user_behaviour():
    while True:#not threadStop.is_set():
        user_json = create_test_add_user_json()
        user_data = json.loads(user_json)
        user_service.add_user(user_json)
        print('User {} added'.format(user_data['email']))
        time.sleep(randint(1,2))
        
        for i in range(randint(0,10)):
            
            session_id = user_service.authenticate_user(create_authentification_data(user_json))
            print('User {} authenticated with session id {}'.format(user_data['email'], session_id))
            time.sleep(randint(1,2))
            for j in range(randint(0,10)):
                user_options[j % 2](user_data[j % 2](user_data['email'], session_id))
                print('User {} option {}'.format(user_data['email']), j % 2)
                time.sleep(randint(1,2))
            user_service.logout_user(create_session_data(user_data['email'], session_id))
            print('User {} logged out'.format(user_data['email']), session_id)
            time.sleep(randint(1,2))
    
        session_id = user_service.authenticate_user(create_authentification_data(user_json))
        print('User {} authenticated with session id {}'.format(user_data['email']), session_id)
        time.sleep(randint(1,2))
        user_service.delete(create_session_data(user_data['email'], session_id))
        print('User {} deleted'.format(user_data['email']), session_id)
        time.sleep(randint(1,2))


if __name__ == '__main__':
    simulate_user_behaviour()
#    threadStop.clear()
#    threads = list()
#    threads.append(threading.Thread(target=simulate_user_behaviour))
#    threads.append(threading.Thread(target=simulate_user_behaviour))
#    threads.append(threading.Thread(target=simulate_user_behaviour))
    
#    for t in threads:
 #       t.start()

  #  for t in threads:
   #     t.join(timeout=10)