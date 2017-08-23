from Exceptions import CommandFailedException

import sys
import os
sys.path.append(os.path.relpath('../mykafka'))
sys.path.append(os.path.relpath('../packet_regex'))

import mykafka
import packet_regex

import json
import codecs
from kafka.errors import KafkaError
import uuid

PACKET_TOPIC = 'packet'

class PostService:
    def __init__(self, producer):
        self.producer = producer
    
    def assign_package_id(self):
        return str(uuid.uuid1())
    
    def register_package(self, jobj):
        print("Register Package")
        packet_regex.check_json_regex(jobj, packet_regex.syntax_register)
        package_id = self.assign_package_id()
        newjobj = { key : value for (key, value) in jobj.items()}
        newjobj['id'] = package_id
        try:
            mykafka.sendSync(self.producer, PACKET_TOPIC, 'registered', 1, newjobj)
        except KafkaError as e:
            raise CommandFailedException("Kafka Error: "+str(e))
        return package_id
    
    def update_package_location(self, jobj):
        print("Update Package Location")
        packet_regex.check_json_regex(jobj, packet_regex.syntax_update)
        try:
            mykafka.sendSync(self.producer, PACKET_TOPIC, 'updated_location', 1, jobj)
        except KafkaError as e:
            raise CommandFailedException("Kafka Error: "+str(e))
        
    def mark_delivered(self, jobj):
        print("Mark delivered", flush=True)
        packet_regex.check_json_regex(jobj, packet_regex.syntax_delivered)
        try:
            mykafka.sendSync(self.producer, PACKET_TOPIC, 'delivered', 1, jobj)
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