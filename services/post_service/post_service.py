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
        self.id_counter = 0
        self.regex_name = '\\w+'
        self.regex_id = '\\d+'
        self.regex_zip = '\\d5'
        self.regex_street = '\\w+'
        self.regex_city = '\\w+'
        self.regex_size = '(small|normal|big)'
        self.regex_weight = '[+-]?(\\d*\\.)?\\d+'
        self.regex_station = '\\w+'
        self.syntax_register = [('sender_name', self.regex_name),
                                ('sender_street',self.regex_street), 
                                ('sender_ZIP', self.regex_zip), 
                                ('sender_city', self.regex_city), 
                                ('receiver_street', self.regex_street), 
                                ('receiver_city', self.regex_city), 
                                ('size', self.regex_size), 
                                ('weight', self.regex_weight)]
        self.syntax_update = [('packet_id', self.regex_id),
                              ('station', self.regex_station)]
        self.syntax_delivered = [('packet_id', self.regex_id)]
        
        
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
        id = self.id_counter
        self.id_counter = self.id_counter+1
        return id
    
    def register_package(self, jobj):
        self.checkAvailable(jobj, self.syntax_register)
        package_id = self.assign_package_id()
        jobj['id'] = package_id
        mykafka.sendSync(self.producer, 'package', 'registered', 1, jobj)
        return package_id
    
    def update_package_location(self, jobj):
        self.checkAvailable(jobj, self.syntax_update)
        mykafka.sendSync(self.producer, 'package', 'updated_location', 1, jobj)
        
    def mark_delivered(self, jobj):
        self.checkAvailable(jobj, self.syntax_delivered)
        mykafka.sendSync(self.producer, 'delivered', 1, jobj)