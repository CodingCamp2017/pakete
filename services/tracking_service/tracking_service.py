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
    
    def __init__(self, id, packageSize, packageWeight, senderName, 
                 senderStreet, senderZip, senderCity, receiverName, 
                 receiverStreet, receiverZip, receiverCity):
        self.id = id
        self.packageSize = packageSize
        self.packageWeight = packageWeight
        
        self.senderName = senderName
        self.senderStreet = senderStreet
        self.senderZip = senderZip
        self.senderCity = senderCity
        
        self.receiverName = receiverName
        self.receiverStreet = receiverStreet
        self.receiverZip = receiverZip
        self.receiverCity = receiverCity
class PackageStore:
    packages = list()
    
    def addPackage(self, event):        
        try:
            packageInformation = json.loads(event)  
        except (Exception) as e:
            print("Event could not be parsed.")
            return False
        
        try:
            payload = packageInformation['payload']
            
            packageId = payload['id']
            packageSize = payload['size']
            packageWeight = payload['weight']
            
            senderName = payload['sender_name']
            senderStreet = payload['sender_street']
            senderZip = payload['sender_zip']
            senderCity = payload['sender_city']
            
            receiverName = payload['receiver_name']
            receiverStreet = payload['receiver_street']
            receiverZip = payload['receiver_zip']
            receiverCity = payload['receiver_city']
            
        except (Exception) as e:
            print("Missing information in event.")
            return False
                
        package = Package(packageId, packageSize, packageWeight, senderName, 
                 senderStreet, senderZip, senderCity, receiverName, 
                 receiverStreet, receiverZip, receiverCity)
        self.packages.append(package)
        
        print('Added package with id: ' + str(packageId))
        
        return True
        
    def findPackage(self, id):
        for p in self.packages:
            if(p.id == id):
                return p
        
    def packageStatus(self, id):
        package = self.findPackage(id)

        if package is None:
            print("Package not found.")
            return
                    
        packageDict = dict()
        
        packageDict.update({'id':str(id)})
        packageDict.update({'size':str(package.packageSize)})
        packageDict.update({'weight':str(package.packageWeight)})
                
        packageDict.update({'sender_name':str(package.senderName)})
        packageDict.update({'sender_street':str(package.senderStreet)})
        packageDict.update({'sender_zip':str(package.senderZip)})
        packageDict.update({'sender_city':str(package.senderCity)})
        
        packageDict.update({'receiver_name':str(package.receiverName)})
        packageDict.update({'receiver_street':str(package.receiverStreet)})
        packageDict.update({'receiver_zip':str(package.receiverZip)})
        packageDict.update({'receiver_city':str(package.receiverCity)})

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
            if dictPackageStatus is None:
                return
                
            try:
                strPackageStatus = json.dumps(dictPackageStatus)
                
            except(Exception) as e:
                return
            
            return strPackageStatus
