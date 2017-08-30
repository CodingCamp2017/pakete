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
        self.idstore = IDStore()
        self.updater = IDUpdater(self.idstore)
        self.updater.start()
    '''
    Returns a uuid used as packet identifier
    '''
    def assign_packet_id(self):
        return str(uuid.uuid4())
    
    '''
    Sends a register event to kafka and thereby registers a packet. jobj is a
    dictionary that contains the data needed.
    Returns a generated packet_id.
    Raises Exception.InvalidActionException if jobj contains an invalid value or is missing a key
    Raises Exception.CommandFailedException if the underlying kafka service could not acknowledge the event
    '''
    def register_packet(self, jobj):
        #print("Register packet: "+str(jobj))
        packet_regex.check_json_regex(jobj, packet_regex.syntax_register)
        packet_id = self.assign_packet_id()
        newjobj = { key : value for (key, value) in jobj.items()}
        newjobj['packet_id'] = packet_id
        try:
            mykafka.sendSync(self.producer, PACKET_TOPIC, PACKET_STATE_REGISTERED, VERSION, newjobj)
        except KafkaError as e:
            raise Exceptions.CommandFailedException("Kafka Error: "+str(e))
        return packet_id
    
    '''
    Updates the location of a packet by sending a updateLocation event to kafka. jobj is a
    dictionary that contains the data needed.
    Returns a generated packet_id.
    Raises Exception.InvalidActionException if jobj contains an invalid value or is missing a key
    Raises Exception.CommandFailedException if the underlying kafka service could not acknowledge the event
    '''
    def update_packet_location(self, jobj):
        #print("Update packet Location: "+str(jobj))
        packet_id = jobj["packet_id"]
        if not self.idstore.check_packet_state(packet_id, PACKET_STATE_UPDATE_LOCATION):
            raise Exceptions.InvalidActionException(Exceptions.TYPE_INVALID_KEY, "packet_id", "Packet with id '"+packet_id+"' has not yet been registered or has been delivered")
        packet_regex.check_json_regex(jobj, packet_regex.syntax_update)
        try:
            mykafka.sendSync(self.producer, PACKET_TOPIC, PACKET_STATE_UPDATE_LOCATION, VERSION, jobj)
        except KafkaError as e:
            raise Exceptions.CommandFailedException("Kafka Error: "+str(e))
    
    '''
    Sends a mark as delivered event to kafka. jobj is a
    dictionary that contains the data needed.
    Returns a generated packet_id.
    Raises Exception.InvalidActionException if jobj contains an invalid value or is missing a key
    Raises Exception.CommandFailedException if the underlying kafka service could not acknowledge the event
    '''
    def mark_delivered(self, jobj):
        #print("Mark delivered: "+str(jobj))
        packet_regex.check_json_regex(jobj, packet_regex.syntax_delivered)
        packet_id = jobj["packet_id"]
        if not self.idstore.check_packet_state(packet_id, PACKET_STATE_UPDATE_LOCATION):
            raise Exceptions.InvalidActionException(Exceptions.TYPE_INVALID_KEY, "packet_id", "Packet with id '"+packet_id+"' has not yet been registered or has been delivered")
        try:
            mykafka.sendSync(self.producer, PACKET_TOPIC, PACKET_STATE_DELIVERED, 2, jobj)
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
