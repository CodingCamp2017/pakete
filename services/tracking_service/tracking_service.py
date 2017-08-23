# -*- coding: utf-8 -*-
#from Exceptions import InvalidActionException, CommandFailedException

import sys
import os
sys.path.append(os.path.relpath('../mykafka'))

import mykafka
import json
import threading

class PacketStation:
    time = ""
    location = ""
    vehicle = ""
    
    def __init(self, time, location, vehicle):
        self.time = time
        self.location = location
        self.vehicle = vehicle

class Packet:
    stations = list()
    
    def __init__(self, id, packetSize, packetWeight, senderName, 
                 senderStreet, senderZip, senderCity, receiverName, 
                 receiverStreet, receiverZip, receiverCity):
        self.id = id
        self.packetSize = packetSize
        self.packetWeight = packetWeight
        
        self.senderName = senderName
        self.senderStreet = senderStreet
        self.senderZip = senderZip
        self.senderCity = senderCity
        
        self.receiverName = receiverName
        self.receiverStreet = receiverStreet
        self.receiverZip = receiverZip
        self.receiverCity = receiverCity
        
    def updateLocation(self, time, location, vehicle):
        self.stations.append(PacketStation(time, location, vehicle))
        
class PacketStore:
    packets = list()
    
    def addPacket(self, eventTime, eventPayload):        
        try:            
            packetId = eventPayload['id']
            packetSize = eventPayload['size']
            packetWeight = eventPayload['weight']
            
            senderName = eventPayload['sender_name']
            senderStreet = eventPayload['sender_street']
            senderZip = eventPayload['sender_zip']
            senderCity = eventPayload['sender_city']
            
            receiverName = eventPayload['receiver_name']
            receiverStreet = eventPayload['receiver_street']
            receiverZip = eventPayload['receiver_zip']
            receiverCity = eventPayload['receiver_city']
            
        except (Exception) as e:
            print("Missing information in register event.")
            return False
                
        packet = Packet(packetId, packetSize, packetWeight, senderName, 
                 senderStreet, senderZip, senderCity, receiverName, 
                 receiverStreet, receiverZip, receiverCity)
        self.packets.append(packet)
        
        print('Added packet with id: ' + str(packetId))
        
        return True
        
    def updatePacket(self, eventTime, eventPayload):
        print("UPDATE: " + str(eventPayload))
        
        try:
            packet_id = eventPayload['packet_id']
            stationLocation = eventPayload['station']
            stationVehicle = eventPayload['vehicle']
        except(Exception) as e:
            print("Missing information in update event.")
            return
            
        packet = self.findPacket(packet_id)
        
        if(packet is None):
            print("Packet not found")
            return
            
        packet.updateLocation(eventTime, stationLocation, stationVehicle)
        print("Successfully updated packet location.")

    def findPacket(self, id):
        for p in self.packets:
            if(p.id == id):
                return p
        
    def packetStatus(self, id):
        packet = self.findPacket(id)

        if packet is None:
            print("Packet not found.")
            return
                    
        packetDict = dict()
        
        packetDict.update({'id':str(id)})
        packetDict.update({'size':str(packet.packetSize)})
        packetDict.update({'weight':str(packet.packetWeight)})
                
        packetDict.update({'sender_name':str(packet.senderName)})
        packetDict.update({'sender_street':str(packet.senderStreet)})
        packetDict.update({'sender_zip':str(packet.senderZip)})
        packetDict.update({'sender_city':str(packet.senderCity)})
        
        packetDict.update({'receiver_name':str(packet.receiverName)})
        packetDict.update({'receiver_street':str(packet.receiverStreet)})
        packetDict.update({'receiver_zip':str(packet.receiverZip)})
        packetDict.update({'receiver_city':str(packet.receiverCity)})
        

        return packetDict
        
    def toString(self):
        s = ""
        
        for p in self.packets:
            s = s + str(p.id) + "\n"
        return s
        

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
            
        # read the whole kafka log and create packet model
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
