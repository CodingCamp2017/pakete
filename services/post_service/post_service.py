from Exceptions import CommandFailedException, InvalidActionException
import Exceptions

import sys
import os
sys.path.append(os.path.relpath('../mykafka'))
sys.path.append(os.path.relpath('../packet_regex'))

import mykafka
import packet_regex
from id_store import IDStore, IDUpdater

import json
import codecs
from kafka.errors import KafkaError
import uuid

STATE_REGISTERED = 'registered'
STATE_UPDATE_LOCATION = 'updated_location'
STATE_DELIVERED = 'delivered'

PACKET_TOPIC = 'packet'

class PostService:
    def __init__(self, producer):
        self.producer = producer
        self.idstore = IDStore()
        self.updater = IDUpdater(self.idstore)
        self.updater.start()
    
    def assign_package_id(self):
        return str(uuid.uuid1())
    
    def register_package(self, jobj):
        print("Register Package: "+str(jobj))
        packet_regex.check_json_regex(jobj, packet_regex.syntax_register)
        package_id = self.assign_package_id()
        newjobj = { key : value for (key, value) in jobj.items()}
        newjobj['id'] = package_id
        try:
            mykafka.sendSync(self.producer, PACKET_TOPIC, STATE_REGISTERED, 2, newjobj)
        except KafkaError as e:
            raise CommandFailedException("Kafka Error: "+str(e))
        return package_id
    
    def update_package_location(self, jobj):
        print("Update Package Location: "+str(jobj))
        packet_regex.check_json_regex(jobj, packet_regex.syntax_update)
        packet_id = jobj["packet_id"]
        if not self.idstore.check_package_state(packet_id, STATE_UPDATE_LOCATION):
            raise InvalidActionException(Exceptions.TYPE_INVALID_KEY, "packet_id", "Packet with id '"+packet_id+"' has not yet been registered or has been delivered")
        try:
            mykafka.sendSync(self.producer, PACKET_TOPIC, STATE_UPDATE_LOCATION, 2, jobj)
        except KafkaError as e:
            raise CommandFailedException("Kafka Error: "+str(e))
        
    def mark_delivered(self, jobj):
        print("Mark delivered: "+str(jobj))
        packet_regex.check_json_regex(jobj, packet_regex.syntax_delivered)
        packet_id = jobj["packet_id"]
        if not self.idstore.check_package_state(packet_id, STATE_UPDATE_LOCATION):
            raise InvalidActionException(Exceptions.TYPE_INVALID_KEY, "packet_id", "Packet with id '"+packet_id+"' has not yet been registered or has been delivered")
        try:
            mykafka.sendSync(self.producer, PACKET_TOPIC, STATE_DELIVERED, 2, jobj)
        except KafkaError as e:
            raise CommandFailedException("Kafka Error: "+str(e))
        
        
def test_regex():
    fakedata = json.load(codecs.open('fakedata.json', 'r', 'utf-8-sig'))['data']
    post_service = PostService(mykafka.create_producer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092))

    for i in range(len(fakedata)-1):
        if not packet_regex.regex_matches_exactly(post_service.regex_name, fakedata[i]['name']):
            print('Name \'' + fakedata[i]['name'] + '\' does not match regex.')
        if not packet_regex.regex_matches_exactly(post_service.regex_street, fakedata[i]['street']):
            print('Street \'' + fakedata[i]['street'] + '\' does not match regex.')
        if not packet_regex.regex_matches_exactly(post_service.regex_city, fakedata[i]['city']):
            print('City \'' + fakedata[i]['city'] + '\' does not match regex.')
        if not packet_regex.regex_matches_exactly(post_service.regex_weight, str(fakedata[i]['weight'])):
            print('Weight \'' + fakedata[i]['weight'] + '\' does not match regex.')
            
if __name__ == '__main__':
    test_regex()