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
    packet_id: The packet_id of this packet
    registration_time: timestamp when this packet was registered
    size: string: size of packet
    weight: floating number: the weight of the packet
    sender_name, sender_street, sender_city, receiver_name, receiver_street, receiver_city: string
    sender_zip, receiver_zip: int
    '''
    def __init__(self, packet_id, registration_time, size, weight, sender_name, 
                 sender_street, sender_zip, sender_city, receiver_name, 
                 receiver_street, receiver_zip, receiver_city):
        self.packet_id = packet_id
        self.registration_time = registration_time
        self.size = size
        self.weight = weight
        
        self.sender_name = sender_name
        self.sender_street = sender_street
        self.sender_zip = sender_zip
        self.sender_city = sender_city
        
        self.receiver_name = receiver_name
        self.receiver_street = receiver_street
        self.receiver_zip = receiver_zip
        self.receiver_city = receiver_city
        
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
        
        pDict.update({'packet_id':str(self.packet_id)})
        pDict.update({'registration_time': str(self.registration_time)})
        pDict.update({'size':str(self.size)})
        pDict.update({'weight':str(self.weight)})
                
        pDict.update({'sender_name':str(self.sender_name)})
        pDict.update({'sender_street':str(self.sender_street)})
        pDict.update({'sender_zip':str(self.sender_zip)})
        pDict.update({'sender_city':str(self.sender_city)})
        
        pDict.update({'receiver_name':str(self.receiver_name)})
        pDict.update({'receiver_street':str(self.receiver_street)})
        pDict.update({'receiver_zip':str(self.receiver_zip)})
        pDict.update({'receiver_city':str(self.receiver_city)})
        
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
            packet_id = eventPayload['packet_id']
            size = eventPayload['size']
            weight = eventPayload['weight']
            registration_time = eventTime
            
            sender_name = eventPayload['sender_name']
            sender_street = eventPayload['sender_street']
            sender_zip = eventPayload['sender_zip']
            sender_city = eventPayload['sender_city']
            
            receiver_name = eventPayload['receiver_name']
            receiver_street = eventPayload['receiver_street']
            receiver_zip = eventPayload['receiver_zip']
            receiver_city = eventPayload['receiver_city']
            
        except (Exception) as e:
            print("Missing information in register event.")
            return False
                
        packet = Packet(packet_id, registration_time, size, weight, sender_name, 
                 sender_street, sender_zip, sender_city, receiver_name, 
                 receiver_street, receiver_zip, receiver_city)
        self.packets.append(packet)
        
        #print('Added packet with packet_id: ' + str(packet_id))
        
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
        #print("Updated packet (packet_id=" + packet_id + ") location to " + stationLocation + ".")

    '''
    Marks a packet as delivered.
    eventTime: timestamp of the delivered event
    eventPayload: the payload data of the delivered event
    '''
    def packetDelivered(self, eventTime, eventPayload):
        try:
            packet_id = eventPayload['packet_id']
        except(Exception) as e:
            print("Missing packet packet_id in update event.")
            return
        
        packet = self.findPacket(packet_id)
        
        if(packet is None):
            print("Packet not found")
            return
            
        packet.setDelivered(eventTime)
        if self.deliverCallback:
            self.deliverCallback(packet_id, eventTime)
        #print("Packet (packet_id: " + packet_id + ") delivered, time " + str(eventTime))
    
    '''
    Returns the Packet with the given packet_id, or None if no packet has the given packet_id
    '''
    def findPacket(self, packet_id):
        for p in self.packets:
            if(str(p.packet_id) == str(packet_id)):
                return p
        return None
        
    '''
    Returns the a dictionary containing all information about the packet with the
    given packet_id.
    Returns None if no packet with the given packet_id was found
    '''
    def packetStatus(self, packet_id):
        packet = self.findPacket(packet_id)

        if packet is None:
            print("Packet not found.")
            return None

        return packet.toJson()
        
    def toString(self):
        s = ""
        
        for p in self.packets:
            s = s + str(p.packet_id) + "\n"
        return s