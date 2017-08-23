# -*- coding: utf-8 -*-
#from Exceptions import InvalidActionException, CommandFailedException

import sys
import os
sys.path.append(os.path.relpath('../mykafka'))

import mykafka
import json
import threading

from packet_model import PacketStore

class TrackingService:
        packetStore = PacketStore()
    
        def __init__(self, consumer):
            self.consumer = consumer
            self.consumerThread = 0
            
            self.readPackets()
             
        def startConsuming(self):
            mykafka.readFromStart(self.consumer, self)
            
        def consumeEvent(self, event):
            eventJson = json.loads(event)  
            
            try:
                eventVersion = eventJson['version']
                eventType = eventJson['type']
                eventTime = eventJson['time']
                eventPayload = eventJson['payload']
            except(Exception) as e:
                print('Event information missing.')
                return
                
            if eventVersion != 1:
                print('Unexpected event version (expected: 1, found: ' + str(eventVersion) + ')')
                return
                
            if eventType == 'registered':
                self.packetStore.addPacket(eventTime, eventPayload)
            
            if eventType == 'updated_location':
                self.packetStore.updatePacket(eventTime, eventPayload)
            
        # start consuming the whole kafka log to create packet model
        def readPackets(self):
            print('Starting packet reading...')
            
            if(self.consumerThread == 0):
                self.consumerThread = threading.Thread(target=self.startConsuming)
                self.consumerThread.start()
                return "Consumer started and reading packets."
            else:
                return "Consumer already running."
            

        def packetStatus(self, packet_id):
            dictPacketStatus = self.packetStore.packetStatus(packet_id)
            if dictPacketStatus is None:
                return
                
            try:
                strPacketStatus = json.dumps(dictPacketStatus)
                
            except(Exception) as e:
                return
            
            return strPacketStatus
