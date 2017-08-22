# -*- coding: utf-8 -*-
from Exceptions import InvalidActionException, CommandFailedException

import sys
import os
sys.path.append(os.path.relpath('../mykafka'))

import mykafka
import re
import json
import threading

class Package:
    id = ""
    senderName = ""
    
    def __init__(self, id, senderName):
        self.id = id
        self.senderName = senderName
    
class PackageStore:
    packages = list()
    
    def addPackage(self, event):
        print('event message: ' + event)
        
        try:
            packageInformation = json.loads(event)  
        except (Exception) as e:
            print('wrong event')
            return
        
        try:
            payload = packageInformation['payload']
            id = payload['id']
            senderName = payload['sender_name']
        except (Exception) as e:
            print('Missing information')
            return
        
        # TODO extract information from the event (= json)
        
        package = Package(id, senderName)
        self.packages.append(package)
        
    def findPackage(self, id):
        for p in self.packages:
            print(p.id)
            if(p.id == id):
                return p
        
    def packageStatus(self, id):
        package = self.findPackage(id)

        if package is None:
            return "Package not found"
                    
        packageDict = dict()
        
        packageDict.update({'id':str(id)})
        packageDict.update({'sender_name':str(package.senderName)})

        return packageDict
        
    def toString(self):
        s = ""
        
        for p in self.packages:
            #s = "%s %s \n" % (s, p.id)            
            s = s + str(p.id) + "\n"
        return s
        

class TrackingService:
        packageStore = PackageStore()
    
        def __init__(self, consumer):
            self.consumer = consumer
            self.consumerThread = 0
             
        def start_consuming(self):
            mykafka.read_from_start(self.consumer, self)
            
        # read the whole kafka log and create package model
        def read_packages(self):
            print('read_packages')
            
            if(self.consumerThread == 0):
                self.consumerThread = threading.Thread(target=self.start_consuming)
                self.consumerThread.start()
            
            return "blub"

        def package_status(self, package_id):
            return self.packageStore.packageStatus(package_id)
