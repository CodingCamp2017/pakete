
import sys
import os
sys.path.append(os.path.relpath('../mykafka'))
sys.path.append(os.path.relpath('../packet_regex'))
import mykafka
import packet_regex

from Exceptions import UserExistsException, UserUnknownException, InvalidSessionIdException, SessionElapsedException, InvalidPasswortException
import sqlite3 as sql
from passlib.hash import pbkdf2_sha256
from datetime import datetime
import json
import uuid

class UserService:
    
    def __init__(self,producer):
        os.system('sqlite3 user_database.db < user_database_schema.sql')
        os.system('sqlite3 followed_packets_database.db < followed_packets_database_schema.sql')
        self.u_con = sql.connect('user_database.db', check_same_thread=False)
        self.u_cur = self.u_con.cursor()
        self.p_con = sql.connect('followed_packets_database.db', check_same_thread=False)
        self.p_cur = self.p_con.cursor()
        self.producer = producer
                
    def _user_exists(self, email):
        self.u_cur.execute('SELECT EXISTS(SELECT 1 FROM users WHERE email=?)', (email,))
        return self.u_cur.fetchone()[0]
            
    def _session_active(self, email, session_id):
        self.u_cur.execute('SELECT session_id, session_id_timestamp FROM users WHERE email=?', (email,))
        [user_session_id, session_id_timestamp] = self.u_cur.fetchone()
        if user_session_id != session_id :
            raise InvalidSessionIdException
        elapsed_time = datetime.now() - datetime.strptime(session_id_timestamp, '%Y-%m-%d %H:%M:%S.%f')
        return elapsed_time.total_seconds() < 600
    
    def _update_session_id_timestamp(self, email, session_id):
        self.u_cur.execute('UPDATE users SET session_id_timestamp = ? WHERE email = ?',
                           (str(datetime.now()), email))
        
    def _check_user_valid_session_active(self, email, session_id):
        if not self._user_exists(email):
            raise UserUnknownException
        if not self._session_active(email, session_id):
            raise SessionElapsedException
        
    def add_user(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_add_user)
        if self._user_exists(data['email']):
            raise UserExistsException
        
        password_hash = pbkdf2_sha256.hash(data['password'])
        self.u_cur.execute('INSERT INTO users (email, password, name, street, zip, city, session_id, session_id_timestamp) VALUES (?,?,?,?,?,?,?,?)',
                           (data['email'], password_hash, '', '', '', '', '', ''))
        self.u_con.commit()

        mykafka.sendSync(self.producer, 'user', 'user_added', 1, data)
    
    def authenticate_user(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_authenticate_user)
        if not self._user_exists(data['email']):
            raise UserUnknownException
        self.u_cur.execute('SELECT (password) FROM users WHERE email=?',
                         (data['email'],))
        password_hash = self.u_cur.fetchone()[0]
        if not pbkdf2_sha256.verify(data['password'], password_hash):
            raise InvalidPasswortException
        session_id = str(uuid.uuid1())
        self.u_cur.execute('UPDATE users SET (session_id, session_id_timestamp) = (?,?) WHERE email = ?',
                           (session_id, str(datetime.now()), data['email']))
        self.u_con.commit()
        return session_id

    def update_user_adress(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_update_user_adress)
        self._check_user_valid_session_active(data['email'], data['session_id'])
        self.u_cur.execute('UPDATE users SET (street, zip, city) = (?,?,?) WHERE email = ?',
                           (data['street'], data['zip'], data['city'], data['email']))
        self.u_con.commit()
        self._update_session_id_timestamp(data['email'], data['session_id'])
    
    def add_packet_to_user(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_add_packet_to_user)
        self._check_user_valid_session_active(data['email'], data['session_id'])
            
        self.p_cur.execute('INSERT INTO followed_packets (email, packet) VALUES (?,?)',
                           (data['email'], data['packet']))
        self.u_con.commit()
        self._update_session_id_timestamp(data['email'], data['session_id'])
        
    def get_packets_from_user(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_get_packets_from_user)
        self._check_user_valid_session_active(data['email'], data['session_id'])
            
        self.p_cur.execute('SELECT (packet) FROM followed_packets WHERE email=?',
                         (data['email'],))
        self._update_session_id_timestamp(data['email'], data['session_id'])
        return self.p_cur.fetchall()
        
    def logout_user(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_get_packets_from_user)
        self._check_user_valid_session_active(data['email'], data['session_id'])
        self.u_cur.execute('UPDATE users SET (session_id, session_id_timestamp) = (?,?) WHERE email = ?',
                           ('', '', data['email']))
        self.u_con.commit()
        
    def delete_user(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_delete_user)
        self._check_user_valid_session_active(data['email'], data['session_id'])
        self.u_cur.execute('DELETE FROM users WHERE email = ?',
                         (data['email'],))
        self.p_cur.execute('DELETE FROM followed_packets WHERE email = ?',
                         (data['email'],))
        self.u_con.commit()
        
    def print_databases(self):
        self.u_cur.execute('SELECT * FROM users')
        print(self.u_cur.fetchall())
        self.p_cur.execute('SELECT * FROM followed_packets')
        print(self.p_cur.fetchall())
        
    def __deinit__(self):
        self.u_con.close()
        self.p_con.close()
        

def create_test_add_user_json():
    data = {'email' : 'karl3@mail.de',
            'name' : 'Karl Müller',
            'street' : 'Amselweg 2',
            'zip' : '12345',
            'city' : 'München-Pasing',
            'password' : 'dadadada'}
    return json.dumps(data)

def create_test_authenticate_user_json():
    data = {'email' : 'karl3@mail.de',
            'password' : 'dadadada'}
    return json.dumps(data)

def create_test_update_user_adress_json(session_id):
    data = {'email' : 'karl3@mail.de',
            'street' : 'Meisenweg 3',
            'zip' : '54321',
            'city' : 'New York',
            'session_id' : session_id}
    return json.dumps(data)

def create_test_delete_user_json(session_id):
    data = {'email' : 'karl3@mail.de',
            'session_id' : session_id}
    return json.dumps(data)

def create_test_get_packets_from_user_json(session_id):
    data = {'email' : 'karl3@mail.de',
            'session_id' : session_id}
    return json.dumps(data)

def create_test_add_packet_to_user_json(session_id):
    data = {'email' : 'karl3@mail.de',
            'packet' : str(uuid.uuid1()),
            'session_id' : session_id}
    return json.dumps(data)
    
def test_user_service():
    
    user_service = UserService(mykafka.create_producer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092))
    
    # test add user
    test_add_user_json = create_test_add_user_json()
    user_service.add_user(test_add_user_json)
    
    # test authenticate user
    test_authenticate_user_json = create_test_authenticate_user_json()
    session_id = user_service.authenticate_user(test_authenticate_user_json)
    
    # test update user adress
    test_update_user_adress_json = create_test_update_user_adress_json(session_id)
    user_service.update_user_adress(test_update_user_adress_json)
  
    # test add packet to user
    test_add_packet_to_user_json = create_test_add_packet_to_user_json(session_id)
    user_service.add_packet_to_user(test_add_packet_to_user_json)
    
    # test get packets from user
    test_get_packets_from_user_json = create_test_get_packets_from_user_json(session_id)
    user_service.get_packets_from_user(test_get_packets_from_user_json)
        
    # test delete user
    test_delete_user_json = create_test_delete_user_json(session_id)
    user_service.delete_user(test_delete_user_json)


if __name__ == '__main__':
    test_user_service()
