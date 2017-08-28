# -*- coding: utf-8 -*-

'''
Represents a delivery center
'''
class PacketStation:
    
    '''
    time: the timestamp when the packet was delivered to this station
    location: the location of this station
    vehicle: the type of transport
    '''
    def __init__(self, time, location, vehicle):
        self.time = time
        self.location = location
        self.vehicle = vehicle
    
    '''
    Returns a dictionary containing relevant information about this station
    '''
    def toJson(self):
        info = {}
        info.update({'time':str(self.time)})
        info.update({'location':str(self.location)})
        info.update({'vehicle':str(self.vehicle)})
        return info

'''
Represents a packet that was registered. This packet can be updated and 
set to be delivered
'''
class Packet:
    
    '''
    packetId: The id of this packet
    packetRegistrationTime: timestamp when this packet was registered
    packetSize: string: size of packet
    packetWeight: floating number: the weight of the packet
    senderName, senderStreet, senderCity, receiverName, receiverStreet, receiverCity: string
    senderZIP, receiverZIP: int
    '''
    def __init__(self, packetId, packetRegistrationTime, packetSize, packetWeight, senderName, 
                 senderStreet, senderZip, senderCity, receiverName, 
                 receiverStreet, receiverZip, receiverCity):
        self.packetId = packetId
        self.packetRegistrationTime = packetRegistrationTime
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
        
        self.stations = list()
        self.deliveryTime = None
    
    '''
    Updates the location of this packet.
    time: timestamp
    location: string, the new location
    vehicle: string, the transport type
    '''
    def updateLocation(self, time, location, vehicle):
        station = PacketStation(time, location, vehicle)
        self.stations.append(station)
        
    '''
    Marks this packet as delivered.
    time: timestamp
    '''
    def setDelivered(self, time):
        self.deliveryTime = time    
    
    '''
    Returns a dictionary containing relevant data
    '''
    def toJson(self):
        pDict = dict()
        
        pDict.update({'id':str(self.packetId)})
        pDict.update({'packetRegistrationTime': str(self.packetRegistrationTime)})
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
    
    '''
    Returns a list of dictionaries containing data describing the way this packet
    took during delivery.
    The dictionaries are created using PacketStation.toJson()
    '''
    def stationsList(self):
        l = list()
        for station in self.stations:
            l.append(station.toJson())
        return l

'''
Stores the history of each packet of the topic
'''
class PacketStore:
    def __init__(self, updateCallback = None, deliverCallback = None):
        self.packets = list()
        self.updateCallback = updateCallback
        self.deliverCallback = deliverCallback
    
    '''
    Adds a packet.
    Returns True if this packet was successfully added, otherwise false
    eventTime: timestamp of the register event
    eventPayload: the payload data of the register event
    '''
    def addPacket(self, eventTime, eventPayload):        
        try:            
            packetId = eventPayload['id']
            packetSize = eventPayload['size']
            packetWeight = eventPayload['weight']
            packetRegistrationTime = eventTime
            
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
                
        packet = Packet(packetId, packetRegistrationTime, packetSize, packetWeight, senderName, 
                 senderStreet, senderZip, senderCity, receiverName, 
                 receiverStreet, receiverZip, receiverCity)
        self.packets.append(packet)
        
        #print('Added packet with id: ' + str(packetId))
        
        return True
        

    '''
    Updates a packet.
    eventTime: timestamp of the updateLocation event
    eventPayload: the payload data of the updateLocation event
    '''
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
        if self.updateCallback:
            self.updateCallback(packet_id, eventTime, stationLocation, stationVehicle)
        #print("Updated packet (id=" + packet_id + ") location to " + stationLocation + ".")

    '''
    Marks a packet as delivered.
    eventTime: timestamp of the delivered event
    eventPayload: the payload data of the delivered event
    '''
    def packetDelivered(self, eventTime, eventPayload):
        try:
            packetId = eventPayload['packet_id']
        except(Exception) as e:
            print("Missing packet id in update event.")
            return
        
        packet = self.findPacket(packetId)
        
        if(packet is None):
            print("Packet not found")
            return
            
        packet.setDelivered(eventTime)
        if self.deliverCallback:
            self.deliverCallback(packetId, eventTime)
        #print("Packet (id: " + packetId + ") delivered, time " + str(eventTime))
    
    '''
    Returns the Packet with the given packetId, or None if no packet has the given id
    '''
    def findPacket(self, packetId):
        for p in self.packets:
            if(str(p.packetId) == str(packetId)):
                return p
        return None
        
    '''
    Returns the a dictionary containing all information about the packet with the
    given packetId.
    Returns None if no packet with the given id was found
    '''
    def packetStatus(self, packetId):
        packet = self.findPacket(packetId)

        if packet is None:
            print("Packet not found.")
            return None

        return packet.toJson()
        
    def toString(self):
        s = ""
        
        for p in self.packets:
            s = s + str(p.id) + "\n"
        return s