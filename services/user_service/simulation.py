from user_service import UserService
from random import randint, sample
import string

import codecs
import json
import sys
import os
sys.path.append(os.path.relpath('../common'))
import uuid
from Exceptions import UserExistsException

char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
sizes = ['small','normal','big']
fakedata = json.load(codecs.open('fakedata.json', 'r', 'utf-8-sig'))['data']


def create_test_user():
    user = fakedata[randint(0, len(fakedata)-1)]
    data = {'email' : user['name'].replace(' ','.').replace('-', '_')+'@mail.de',
            'password' : ''.join(sample(char_set*8, 8))}
    return data

def create_simple_test_user():
    return {'email' : 'karl3@mail.de', 'password' : '12345678'}


def create_add_packet_data(session_id):
    return {'packet' : str(uuid.uuid1()),
            'session_id' : session_id}


def simulate_user_behaviour():
    user_service = UserService()
    
    user_service.print_databases()
    
    for i in range(1):
        user_data = create_test_user()
        try:
            user_service.add_user(user_data)
        except UserExistsException:
            continue
        print('User {} added'.format(user_data['email']))
        #time.sleep(randint(1,2))
        
        for i in range(randint(0,10)):
            
            session_id = user_service.authenticate_user(user_data)
            print('User {} authenticated '.format(user_data['email']))
            #time.sleep(randint(1,2))
            for j in range(randint(0,10)):
                if randint(0,1):
                    user_service.add_packet_to_user(create_add_packet_data(session_id))
                    print('User {} added packet'.format(user_data['email']))
                else:
                    packets = user_service.get_packets_from_user(session_id)
                    print('User {} has packets'.format(user_data['email'], packets))
                #time.sleep(randint(1,2))
            user_service.logout_user(session_id)
            print('User {} logged out'.format(user_data['email']))
            #time.sleep(randint(1,2))
    
    user_service.print_databases()


if __name__ == '__main__':
    simulate_user_behaviour()
