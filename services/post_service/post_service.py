import sys
import os
sys.path.append(os.path.relpath('../mykafka'))
sys.path.append(os.path.relpath('../common'))

import Exceptions

import mykafka
import packet_regex
from id_store import IDStore, IDUpdater
from constants import PACKET_TOPIC, PACKET_STATE_REGISTERED, PACKET_STATE_UPDATE_LOCATION, PACKET_STATE_DELIVERED

import json
import codecs
from kafka.errors import KafkaError
import uuid

VERSION = 3
#add all registered packets
add  = lambda state, payload: state == PACKET_STATE_REGISTERED
#remove if delivered
delete = lambda newstate, payload, oldstate: newstate == PACKET_STATE_DELIVERED

'''
The Post-Service provides a web interface to register packets, update their
locations and to mark them as delivered.
'''
class PostService:
    '''
    producer: A producer that is connected to kafka
    '''
    def __init__(self, producer):
        self.producer = producer
        self.idstore = IDStore(VERSION, add, delete)
        self.updater = IDUpdater(self.idstore)
        self.updater.start()
    '''
    Returns a uuid used as packet identifier
    '''
    def assign_packet_id(self):
        return str(uuid.uuid4())
    
    '''
    Sends a register event to kafka and thereby registers a packet. data is a
    dictionary that contains the data needed.
    Returns a generated packet_id.
    Raises Exception.InvalidActionException if data contains an invalid value or is missing a key
    Raises Exception.CommandFailedException if the underlying kafka service could not acknowledge the event
    '''
    def register_packet(self, data):
        #print("Register packet: "+str(data))
        packet_regex.check_json_regex(data, packet_regex.syntax_register)
        packet_id = self.assign_packet_id()
        newdata = { key : value for (key, value) in data.items()}
        newdata['packet_id'] = packet_id
        try:
            mykafka.sendSync(self.producer, PACKET_TOPIC, PACKET_STATE_REGISTERED, VERSION, newdata)
        except KafkaError as e:
            raise Exceptions.CommandFailedException("Kafka Error: "+str(e))
        return packet_id
    
    '''
    Updates the location of a packet by sending a updateLocation event to kafka. data is a
    dictionary that contains the data needed.
    Returns a generated packet_id.
    Raises Exception.InvalidActionException if data contains an invalid value or is missing a key
    Raises Exception.CommandFailedException if the underlying kafka service could not acknowledge the event
    '''
    def update_packet_location(self, data):
        #print("Update packet Location: "+str(data))
        packet_id = data["packet_id"]
        if not self.idstore.packet_in_store(packet_id):
            raise Exceptions.InvalidActionException(Exceptions.TYPE_INVALID_KEY, "packet_id", "Packet with id '"+packet_id+"' has not yet been registered or has been delivered")
        packet_regex.check_json_regex(data, packet_regex.syntax_update)
        try:
            mykafka.sendSync(self.producer, PACKET_TOPIC, PACKET_STATE_UPDATE_LOCATION, VERSION, data)
        except KafkaError as e:
            raise Exceptions.CommandFailedException("Kafka Error: "+str(e))
    
    '''
    Sends a mark as delivered event to kafka. data is a
    dictionary that contains the data needed.
    Returns a generated packet_id.
    Raises Exception.InvalidActionException if data contains an invalid value or is missing a key
    Raises Exception.CommandFailedException if the underlying kafka service could not acknowledge the event
    '''
    def mark_delivered(self, data):
        #print("Mark delivered: "+str(data))
        packet_regex.check_json_regex(data, packet_regex.syntax_delivered)
        packet_id = data["packet_id"]
        if not self.idstore.packet_in_store(packet_id):
            raise Exceptions.InvalidActionException(Exceptions.TYPE_INVALID_KEY, "packet_id", "Packet with id '"+packet_id+"' has not yet been registered or has been delivered")
        try:
            mykafka.sendSync(self.producer, PACKET_TOPIC, PACKET_STATE_DELIVERED, VERSION, data)
        except KafkaError as e:
            raise Exceptions.CommandFailedException("Kafka Error: "+str(e))
        
        
def test_regex():
    fakedata = json.load(codecs.open('fakedata.json', 'r', 'utf-8-sig'))['data']

    for i in range(len(fakedata)-1):
        if not packet_regex.regex_matches_exactly(packet_regex.regex_name, fakedata[i]['name']):
            print('Name \'' + fakedata[i]['name'] + '\' does not match regex.')
        if not packet_regex.regex_matches_exactly(packet_regex.regex_street, fakedata[i]['street']):
            print('Street \'' + fakedata[i]['street'] + '\' does not match regex.')
        if not packet_regex.regex_matches_exactly(packet_regex.regex_city, fakedata[i]['city']):
            print('City \'' + fakedata[i]['city'] + '\' does not match regex.')
        if not packet_regex.regex_matches_exactly(packet_regex.regex_weight, str(fakedata[i]['weight'])):
            print('Weight \'' + fakedata[i]['weight'] + '\' does not match regex.')
            
if __name__ == '__main__':
    test_regex()
