# -*- coding: utf-8 -*-
#from Exceptions import InvalidActionException, CommandFailedException

class PacketStation:
    time = ""
    location = ""
    vehicle = ""
    
    def __init__(self, time, location, vehicle):
        self.time = time
        self.location = location
        self.vehicle = vehicle
        
    def toJson(self):
        info = {}
        info.update({'time':str(self.time)})
        info.update({'location':str(self.location)})
        info.update({'vehicle':str(self.vehicle)})
        return info

class Packet:
    stations = list()
    deliveryTime = None
    
    def __init__(self, packetId, packetSize, packetWeight, senderName, 
                 senderStreet, senderZip, senderCity, receiverName, 
                 receiverStreet, receiverZip, receiverCity):
        self.packetId = packetId
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
        station = PacketStation(time, location, vehicle)
        self.stations.append(station)
        
    def setDelivered(self, time):
        self.deliveryTime = time    
    
    def toJson(self):
        pDict = dict()
        
        pDict.update({'id':str(id)})
        pDict.update({'size':str(self.packetSize)})
        pDict.update({'weight':str(self.packetWeight)})
                
        pDict.update({'sender_name':str(self.senderName)})
        pDict.update({'sender_street':str(self.senderStreet)})
        pDict.update({'sender_zip':str(self.senderZip)})
        pDict.update({'sender_city':str(self.senderCity)})
        
        pDict.update({'receiver_name':str(self.receiverName)})
        pDict.update({'receiver_street':str(self.receiverStreet)})
        pDict.update({'receiver_zip':str(self.receiverZip)})
        pDict.update({'receiver_city':str(self.receiverCity)})
        
        if self.deliveryTime != None:
            pDict.update({'deliveryTime': str(self.deliveryTime)})

        pDict.update({'stations':self.stationsList()})

        return pDict
        
    def stationsList(self):
        l = list()
        for station in self.stations:
            l.append(station.toJson())
        return l
        
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
        print("Updated packet (id=" + packet_id + ") location to " + stationLocation + ".")

    def packetDelivered(self, eventTime, packetId):
        packet = self.findPacket(packetId)
        
        if(packet is None):
            print("Packet not found")
            return
            
        packet.setDelivered(eventTime)
        print("Packet delivered")
            
    def findPacket(self, packetId):
        for p in self.packets:
            if(str(p.packetId) == str(packetId)):
                return p
        
    def packetStatus(self, id):
        packet = self.findPacket(id)

        if packet is None:
            print("Packet not found.")
            return

        return packet.toJson()
        
    def toString(self):
        s = ""
        
        for p in self.packets:
            s = s + str(p.id) + "\n"
        return s