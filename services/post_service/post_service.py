from Exceptions import InvalidActionException, CommandFailedException

import sys
import os
sys.path.append(os.path.relpath('../mykafka'))

import mykafka
import re
import json


class PostService:
    def __init__(self, producer):
        self.producer = producer
        
        
    def regex_matches_exactly(self, regex, string):
        match = re.compile(regex).match(string)
        return match != None and match.end() == len(string)
    
    def checkAvailable(self, dict, req_list):
        for (key, regex) in req_list:
            if(not key in dict):
                raise InvalidActionException("Required key: "+key)
            elif(not self.regex_matches_exactly(regex, dict[key])):
                raise InvalidActionException("Invalid value: "+dict[key]+" for key "+key)
        if(len(dict) == len(req_list)):
            raise InvalidActionException("Unknown keys")
    
    def assign_package_id(self):
        return 0
    
    def register_package(self, jsons):
        jobj = json.dumps(jsons)
        self.checkAvailable(jobj, [])
        package_id = self.assign_package_id()
        jobj['id'] = package_id
        mykafka.send(self.producer, 'package', 'registered', 1, jobj)
        return package_id
    
    def update_package_location(self, jsons):
        jobj = json.dumps(jsons)
        self.checkAvailable(jobj, [])
        mykafka.send(self.producer, 'package', 'updated_location', 1, jobj)
        
    def mark_delivered(self, jsons):
        jobj = json.dumbs(jsons)
        self.checkAvailable(jobj, [])
        mykafka.send(self.producer, 'delivered', 1, jobj)