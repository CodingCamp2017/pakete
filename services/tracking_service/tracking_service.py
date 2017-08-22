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
    id = -1
    
    def __init__(self, id):
        self.id = id
    
class PackageStore:
    packages = list()
    
    def addPackage(self, event):
        id = event # TODO extract information from the event (= json)
        
        self.packages.append(Package(id))
        
    def toString(self):
        s = ""
        
        for p in self.packages:
            s = s + p.id + "\n"
            
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

        def package_status(self, jsons):
            #jobj = ? # convert json string to object
            package_id = 0 # jobj['id']
            #return "status of package" + package_id
            return self.packageStore.toString()