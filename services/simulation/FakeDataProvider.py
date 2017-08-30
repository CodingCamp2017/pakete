import codecs
import json

from random import randint

class FakeDataProvider:

    def __init__(self, filename):
        self.fakedata = json.load(codecs.open(filename, 'r', 'utf-8-sig'))['data']
        self.sizes = ['small','normal','big']
        self.vehicles = ['car', 'foot', 'plane', 'rocket', 'ship', 'train', 'truck', 'center', 'failed']
        self.stations = {0 : {'station' : 'Brief Leipzig', 'zip' : '04158', 'city' : 'Leipzig', 'street': 'Poststr. 28'},
                         1 : {'station' : 'Brief Neubrandenburg', 'zip' : '17235', 'city' : 'Neustrelitz', 'street': 'Bürgerseeweg 27'},
                         2 : {'station' : 'Brief Hamburg-Süd', 'zip' : '21035', 'city' : 'Hamburg', 'street': 'Rungedamm 37'},
                         3 : {'station' : 'Brief Kassel', 'zip' : '34355', 'city' : 'Staufenberg', 'street': 'Im Rotte 2'},
                         4 : {'station' : 'Brief Essen', 'zip' : '46282', 'city' : 'Dorsten', 'street': 'Lünsingskuhle 70'},
                         5 : {'station' : 'Brief Koblenz', 'zip' : '56566', 'city' : 'Neuwied', 'street': 'Rostocker Str. 14'},
                         6 : {'station' : 'Paketzentrum Obertshausen', 'zip' : '63179', 'city' : 'Obertshausen', 'street': 'Im Birkengrund'},
                         7 : {'station' : 'Brief Reutlingen', 'zip' : '72184', 'city' : 'Eutingen im Gäu', 'street': 'Am Flugplatz 14'},
                         8 : {'station' : 'Brief Augsburg', 'zip' : '86154', 'city' : 'Augsburg', 'street': 'Stuttgarter Str. 33'},
                         9 : {'station' : 'Brief Nürnberg', 'zip' : '90475', 'city' : 'Nürnberg', 'street': 'Am Tower 10'}}


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
	    return packet

    def getRandomCity(self):
        return self.fakedata[randint(0, len(self.fakedata)-1)]['city']

    def getRandomVehicle(self):
        return self.vehicles[randint(0,len(self.vehicles)-1)]

    def getRandomStation(self):
        return self.stations[randint(0, len(self.stations)-1)]