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
        try:
            packageInformation = json.loads(event)  
        except (Exception) as e:
            return "Event could not be parsed."
        
        try:
            payload = packageInformation['payload']
            
            packageId = payload['id']
            '''packageSize = payload['size']
            packageWeight = payload['weight']'''
            
            senderName = payload['sender_name']
            '''
            senderStreet = payload['sender_street']
            senderZip = payload['sender_zip']
            senderCity = payload['sender_city']
            
            receiverName = payload['receiver_name']
            receiverStreet = payload['receiver_street']
            receiverZip = payload['receiver_zip']
            receiverCity = payload['receiver_city']'''
            
        except (Exception) as e:
            return "Missing information in event."
        
        # TODO extract information from the event (= json)
        
        package = Package(packageId, senderName)
        self.packages.append(package)
        
        print('Added package with id: ' + str(packageId))
        
        return "Event successfully added."
        
    def findPackage(self, id):
        for p in self.packages:
            if(p.id == id):
                return p
        
    def packageStatus(self, id):
        package = self.findPackage(id)

        if package is None:
            return "Package not found."
                    
        packageDict = dict()
        
        packageDict.update({'id':str(id)})
        packageDict.update({'sender_name':str(package.senderName)})

        return packageDict
        
    def toString(self):
        s = ""
        
        for p in self.packages:
            s = s + str(p.id) + "\n"
        return s
        

class TrackingService:
        packageStore = PackageStore()
    
        def __init__(self, consumer):
            self.consumer = consumer
            self.consumerThread = 0
            
            self.read_packages()
             
        def start_consuming(self):
            mykafka.read_from_start(self.consumer, self)
            
        # read the whole kafka log and create package model
        def read_packages(self):
            print('Starting package reading...')
            
            if(self.consumerThread == 0):
                self.consumerThread = threading.Thread(target=self.start_consuming)
                self.consumerThread.start()
                return "Consumer started and reading packages."
            else:
                return "Consumer already running."
            

        def package_status(self, package_id):
            dictPackageStatus = self.packageStore.packageStatus(package_id)
            try:
                strPackageStatus = json.dumps(dictPackageStatus)
                
            except(Exception) as e:
                return "Unable to parse package status dictionary"
            
            return strPackageStatus
