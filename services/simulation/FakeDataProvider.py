import sys
import os
sys.path.append(os.path.relpath('../common'))

import distribution_center
import codecs
import json
from random import randint


class FakeDataProvider:

    def __init__(self, filename):
        self.fakedata = json.load(codecs.open(filename, 'r', 'utf-8-sig'))['data']
        self.sizes = ['small','normal','big']
        self.vehicles = ['car', 'foot', 'plane', 'rocket', 'ship', 'train', 'truck', 'center', 'failed']
        self.fakenames = json.load(codecs.open('names.json', 'r', 'utf-8-sig'))['names']
        self.fakeaddresses = json.load(codecs.open('addresses.json', 'r', 'utf-8-sig'))['addresses']
        self.stations = list(distribution_center.names.values())


    def getRandomPacket(self):
	    sender = self.fakedata[randint(0, len(self.fakedata)-1)]
	    receiver = self.fakedata[randint(0, len(self.fakedata)-1)]
	    packet = {}
	    packet['sender_name'] = sender['name']
	    packet['sender_street'] = sender['street']
	    packet['sender_zip'] = str(randint(10000,99999))
	    packet['sender_city'] = sender['city']
	    packet['receiver_name'] = receiver['name']
	    packet['receiver_street'] = receiver['street']
	    packet['receiver_zip'] = str(randint(10000,99999))
	    packet['receiver_city'] = receiver['city']
	    packet['size'] = self.sizes[randint(0,len(self.sizes)-1)]
	    packet['weight'] = str(sender['weight'])
	    packet['auto_deliver'] = True
	    return packet

    def getRandomCity(self):
        return self.fakedata[randint(0, len(self.fakedata)-1)]['city']
    
    def getRandomSize(self):
        return self.sizes[randint(0, len(self.sizes)-1)]

    def getRandomVehicle(self):
        return self.vehicles[randint(0,len(self.vehicles)-1)]

    def getRandomStation(self):
        return self.stations[randint(0, len(self.stations)-1)]
    
    def getRandomName(self):
        return self.fakenames[randint(0, len(self.fakenames)-1)]
    
    def getRandomAddress(self):
        return self.fakeaddresses[randint(0, len(self.fakeaddresses)-1)]