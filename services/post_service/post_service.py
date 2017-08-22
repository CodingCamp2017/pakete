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
        self.regex_zip = '\\d{5}'
        self.regex_street = '\\w+'
        self.regex_city = '\\w+'
        self.regex_size = '(small|normal|big)'
        self.regex_weight = '[+-]?(\\d*\\.)?\\d+'
        self.regex_station = '\\w+'
        self.syntax_register = [('sender_name', self.regex_name),
                                ('sender_street',self.regex_street), 
                                ('sender_ZIP', self.regex_zip), 
                                ('sender_city', self.regex_city),
                                ('receiver_name', self.regex_name),
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
    
    def checkAvailable(self, dic, req_list):
        for (key, regex) in req_list:
            if(not key in dic):
                raise InvalidActionException("Required key: "+key)
            elif(not self.regex_matches_exactly(regex, dic[key])):
                raise InvalidActionException("Invalid value: "+dic[key]+" for key "+key)
        if(len(dic) != len(req_list)):
            raise InvalidActionException("Unknown keys in "+json.dumps(dic))
    
    def assign_package_id(self):
        id = self.id_counter
        self.id_counter = self.id_counter+1
        return id
    
    def register_package(self, jobj):
        print("Register Package")
        self.checkAvailable(jobj, self.syntax_register)
        package_id = self.assign_package_id()
        jobj['id'] = package_id
        mykafka.sendSync(self.producer, 'package', 'registered', 1, jobj)
        return package_id
    
    def update_package_location(self, jobj):
        print("Update Package Location")
        self.checkAvailable(jobj, self.syntax_update)
        mykafka.sendSync(self.producer, 'package', 'updated_location', 1, jobj)
        
    def mark_delivered(self, jobj):
        print("Mark delivered", flush=True)
        self.checkAvailable(jobj, self.syntax_delivered)
        mykafka.sendSync(self.producer, 'delivered', 1, jobj)
        
        
def test_checkAvailable():
    req = [("a", "\\d{2}"), ("b", "hgf")]
    dic = {'a':'45', 'b':'hgf'}
    post_service = PostService(None)
    post_service.checkAvailable(dic, req)
    print("test_checkAvailable#1")
    dic['a'] = 'a1'
    try:
        post_service.checkAvailable(dic, req)
        raise AssertionError('test_checkAvailable')
    except InvalidActionException:
        pass
    print("test_checkAvailable#2")
        
    dic2 = {'a':'12', 'b':'fgtd', 'c':'wer'}
    try:
        post_service.checkAvailable(dic2, req)
        raise AssertionError('test_checkAvailable2')
    except InvalidActionException as e:
        pass
    print("test_checkAvailable#3")
    dic3 = {'a':'16'}
    try:
        post_service.checkAvailable(dic3, req)
        raise AssertionError('test_checkAvailable3')
    except InvalidActionException as e:
        pass
    print("test_checkAvailable#4")
        
if __name__ == '__main__':
    test_checkAvailable()
        