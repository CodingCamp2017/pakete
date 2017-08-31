import sys
import os
sys.path.append(os.path.relpath('../common'))
sys.path.append(os.path.relpath('../mykafka'))
import constants
import mykafka
from user_events import UserEvent, UserPacketEvent
from kafka.errors import KafkaError
import packet_regex
from id_store import IDStore, IDUpdater
from Exceptions import *
import sqlite3 as sql
from passlib.hash import pbkdf2_sha256
from datetime import datetime
import uuid

#add all registered packets
add = lambda state, payload: state == constants.PACKET_STATE_REGISTERED
#never remove a packet
delete = lambda newstate, payload, oldstate: False

class UserService:

    def __init__(self, producer):
        self.producer = producer
        if not os.path.isfile('user_database.db'):
            os.system('sqlite3 user_database.db < user_database_schema.sql')
            os.system('sqlite3 followed_packets_database.db < followed_packets_database_schema.sql')
        self.u_con = sql.connect('user_database.db', check_same_thread=False)
        self.u_cur = self.u_con.cursor()
        self.p_con = sql.connect('followed_packets_database.db', check_same_thread=False)
        self.p_cur = self.p_con.cursor()

        try:
            self.u_cur.execute('INSERT INTO users (email, password, name, street, zip, city, session_id, session_id_timestamp) VALUES (?,?,?,?,?,?,?,?)',
                               ('dummy_email', '123', '', '', '', '', '', ''))
        except sql.OperationalError:
            #print('User database is locked')
            os.system('mv user_database.db temp.db')
            os.system('cp temp.db user_database.db')
            self.u_con = sql.connect('user_database.db', check_same_thread=False)
            self.u_cur = self.u_con.cursor()

        try:
            self.p_cur.execute('INSERT INTO followed_packets (email, packet) VALUES (?,?)',
                               ('dummy_email', '123'))
        except sql.OperationalError:
            #print('Packets database is locked')
            os.system('mv followed_packets_database.db temp.db')
            os.system('cp temp.db followed_packets_database.db')
            self.p_con = sql.connect('followed_packets_database.db', check_same_thread=False)
            self.p_cur = self.p_con.cursor()

        self.idstore = IDStore(3, add, delete)
        self.updater = IDUpdater(self.idstore)
        self.updater.start()

    def _user_exists(self, email):
        self.u_cur.execute('SELECT EXISTS(SELECT 1 FROM users WHERE email=?)', (email,))
        return self.u_cur.fetchone()[0]

    def _get_email_of_user(self, session_id):
        self.u_cur.execute('SELECT email FROM users WHERE session_id = ?', (session_id,))
        email = self.u_cur.fetchone()
        if email:
            return email[0]
            
    def _packet_added_to_user(self, email, packet_id):
        #print('checking ' + email + ', id: ' + packet_id)       
        result = self.p_cur.execute('SELECT EXISTS(SELECT 1 FROM followed_packets WHERE email=? AND packet=?)', (email,packet_id,)).fetchone()
        return True if result[0] else False

    '''
    Throws InvalidSessionIdException, SessionElapsedException
    '''
    def _check_session_active(self, session_id):
        self.u_cur.execute('SELECT session_id_timestamp FROM users WHERE session_id=?', (session_id,))
        ids = self.u_cur.fetchone()
        if not ids:
            raise InvalidSessionIdException('session_id invalid')
        session_id_timestamp = ids[0]
        elapsed_time = datetime.now() - datetime.strptime(session_id_timestamp, '%Y-%m-%d %H:%M:%S.%f')
        if elapsed_time.total_seconds() > 600:
            # TODO: remove session id
            raise SessionElapsedException('session elapsed')

    def _update_session_id_timestamp(self, session_id):
        self.u_cur.execute('UPDATE users SET session_id_timestamp = ? WHERE session_id = ?',
                           (str(datetime.now()), session_id))

    '''
    May raise CommandFailedException
    '''
    def _send_user_event(self, event_type, user_event):
        try:
            mykafka.sendSync(self.producer, constants.USER_TOPIC, event_type, constants.USER_EVENT_VERSION, user_event.toDict())
        except KafkaError as e:
            raise CommandFailedException("Kafka Error: "+str(e))

    def add_user(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_add_user)
        if self._user_exists(data['email']):
            raise UserExistsException('This email '+data['email']+' is already in use')

        password_hash = pbkdf2_sha256.hash(data['password'])
        self.u_cur.execute('INSERT INTO users (email, password, name, street, zip, city, session_id, session_id_timestamp) VALUES (?,?,?,?,?,?,?,?)',
                           (data['email'], password_hash, '', '', '', '', '', ''))
        self.u_con.commit()
        #send user event
        self._send_user_event(constants.USER_EVENT_ADD, UserEvent(data['email']))

    def authenticate_user(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_authenticate_user)
        if not self._user_exists(data['email']):
            raise UserUnknownException('This email '+data['email']+' is not registered')
        self.u_cur.execute('SELECT (password) FROM users WHERE email=?',
                         (data['email'],))
        password_hash = self.u_cur.fetchone()[0]
        if not pbkdf2_sha256.verify(data['password'], password_hash):
            raise InvalidPasswortException('Wrong password')
        session_id = str(uuid.uuid1())
        self.u_cur.execute('UPDATE users SET session_id = ? WHERE email = ?',
                           (session_id, data['email']))
        self.u_cur.execute('UPDATE users SET session_id_timestamp = ? WHERE email = ?',
                           (str(datetime.now()), data['email']))
        self.u_con.commit()
        # send user event
        self._send_user_event(constants.USER_EVENT_LOGIN, UserEvent(data['email']))
        return session_id

#    def update_user_adress(self, data):
#        packet_regex.check_json_regex(data, packet_regex.syntax_update_user_adress)
#        self._check_user_valid_session_active(data['email'], data['session_id'])
#        self.u_cur.execute('UPDATE users SET (street, zip, city) = (?,?,?) WHERE email = ?',
#                           (data['street'], data['zip'], data['city'], data['email']))
#        self.u_con.commit()
#        self._update_session_id_timestamp(data['email'], data['session_id'])

    def add_packet_to_user(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_add_packet_to_user)
        self._check_session_active(data['session_id'])
        if not self.idstore.packet_in_store(data['packet_id']):
            raise PacketNotFoundException('No packet with id '+data['packet_id']+' found')
        email = self._get_email_of_user(data['session_id'])
        
        #check if packet already added to user
        if self._packet_added_to_user(email, data['packet_id']):
            raise PacketAlreadyAddedException
        
        self.p_cur.execute('INSERT INTO followed_packets (email, packet) VALUES (?,?)',
                           (email, data['packet_id']))
        self._update_session_id_timestamp(data['session_id'])
        self.u_con.commit()
        # send user event
        email = self._get_email_of_user(data['session_id'])
        if email:
            self._send_user_event(constants.USER_EVENT_ADDED_PACKET, UserPacketEvent(email, data['packet_id']))
    # TODO remove packet from user

    def remove_packet_from_user(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_remove_packet_from_user)
        self._check_session_active(data['session_id'])
        if not self.idstore.packet_in_store(data['packet_id']):
            raise PacketNotFoundException
        email = self._get_email_of_user(data['session_id'])
        
        #check if packet already added to user
        if self._packet_added_to_user(email, data['packet_id']):
            self.p_cur.execute('DELETE FROM followed_packets WHERE email=? AND packet=?',
                               (email, data['packet_id']))
            self._update_session_id_timestamp(data['session_id'])
            self.u_con.commit()
        else:
            raise NoSuchPacketAddedException

    def get_packets_from_user(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_session_id)
        session_id = data['session_id']
        self._check_session_active(session_id)
        self._update_session_id_timestamp(session_id)
        email = self._get_email_of_user(session_id)
        self.p_cur.execute('SELECT (packet) FROM followed_packets WHERE email=?', (email,))
        packets = [p[0] for p in self.p_cur.fetchall()]
        return packets

    def logout_user(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_session_id)
        session_id = data['session_id']
        email = self._get_email_of_user(session_id)
        self._check_session_active(session_id)
        self.u_cur.execute('UPDATE users SET session_id = ? WHERE session_id = ?', ('', session_id))
        self.u_cur.execute('UPDATE users SET session_id_timestamp = ? WHERE session_id = ?', ('', session_id))
        self.u_con.commit()
        if email:
            self._send_user_event(constants.USER_EVENT_LOGOUT, UserEvent(email))

    def delete_user(self, data):
        packet_regex.check_json_regex(data, packet_regex.syntax_session_id)
        session_id = data['session_id']
        self._check_session_active(session_id)
        email = self._get_email_of_user(session_id)
        self.u_cur.execute('DELETE FROM users WHERE session_id = ?', (session_id,))
        self.p_cur.execute('DELETE FROM followed_packets WHERE email = ?', (email,))
        self.u_con.commit()
        self._send_user_event(constants.USER_EVENT_DELETE, UserEvent(email))

    def print_databases(self):
        self.u_cur.execute('SELECT * FROM users')
        print(self.u_cur.fetchall())
        self.p_cur.execute('SELECT * FROM followed_packets')
        print(self.p_cur.fetchall())

    def close(self):
        self.u_con.close()
        self.p_con.close()

    def __del__(self):
        self.u_con.close()
        self.p_con.close()


def create_email_password():
    return {'email' : 'kasrl3@mail.de',
            'password' : 'dadadada'}

def create_email_packet_session(session_id):
    return {'packet_id' : str(uuid.uuid1()),
            'session_id' : session_id}

def create_test_delete_user_json(session_id):
    return {'email' : 'karl3@mail.de',
            'session_id' : session_id}

def create_test_get_packets_from_user_json(session_id):
    return {'email' : 'karl3@mail.de',
            'session_id' : session_id}

def create_test_add_packet(session_id):
    return {'packet_id' : str(uuid.uuid1()),
            'session_id' : session_id}

def test_user_service():

    user_service = UserService()

    test_user = create_email_password()

    # test add user
    user_service.add_user(test_user)

    # test authenticate user
    session_id = user_service.authenticate_user(test_user)

    # test add packet to user
    try:
        user_service.add_packet_to_user(create_test_add_packet(session_id))
    except PacketNotFoundException:
        print('Packet not found')

    # test get packets from user
    user_service.get_packets_from_user(session_id)

    # test delete user
    user_service.delete_user(session_id)


if __name__ == '__main__':
    test_user_service()
