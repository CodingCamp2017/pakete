import sys
import os
sys.path.append(os.path.relpath('../mykafka'))
sys.path.append(os.path.relpath('../post_service'))

import mykafka
import threading
import json
import urllib
import signal
from post_service import PostService
import time
import http.client

from threading import Lock

mylock = Lock()
p = print

def print(*a, **b):
	with mylock:
		p(*a, **b)


distributionCenter = {0 : {'station' : 'Brief Leipzig', 'zip' : '04158', 'city' : 'Leipzig', 'street': 'Poststr. 28'},
                      1 : {'station' : 'Brief Neubrandenburg', 'zip' : '17235', 'city' : 'Neustrelitz', 'street': 'Bürgerseeweg 27'},
                      2 : {'station' : 'Brief Hamburg-Süd', 'zip' : '21035', 'city' : 'Hamburg', 'street': 'Rungedamm 37'},
                      3 : {'station' : 'Brief Kassel', 'zip' : '34355', 'city' : 'Staufenberg', 'street': 'Im Rotte 2'},
                      4 : {'station' : 'Brief Essen', 'zip' : '46282', 'city' : 'Dorsten', 'street': 'Lünsingskuhle 70'},
                      5 : {'station' : 'Brief Koblenz', 'zip' : '56566', 'city' : 'Neuwied', 'street': 'Rostocker Str. 14'},
                      6 : {'station' : 'Paketzentrum Obertshausen', 'zip' : '63179', 'city' : 'Obertshausen', 'street': 'Im Birkengrund'},
                      7 : {'station' : 'Brief Reutlingen', 'zip' : '72184', 'city' : 'Eutingen im Gäu', 'street': 'Am Flugplatz 14'},
                      8 : {'station' : 'Brief Augsburg', 'zip' : '86154', 'city' : 'Augsburg', 'street': 'Stuttgarter Str. 33'},
                      9 : {'station' : 'Brief Nürnberg', 'zip' : '90475', 'city' : 'Nürnberg', 'street': 'Am Tower 10'}}


class DistributionService(threading.Thread):
    
    def __init__(self, center_id, threadStop):
        
        threading.Thread.__init__(self)
        self.center_id = center_id
        self.baseurl = 'ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8000'
        self.headers = {'Content-Type':'application/json'}
        self.threadStop = threadStop
        self.lock = threading.Lock()
        self.post_service = PostService(mykafka.create_producer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092))
        
    def _zip_in_purview(self, zip_code):
        return zip_code[0] == str(self.center_id)
        
    def _transport_packet(self, center_id, vehicle, packet_id):
        with self.lock:
            data = {'vehicle' : vehicle, 'packet_id' : packet_id}
            data.update(distributionCenter[center_id])
            self.post_service.update_package_location(data)
            print(str(packet_id) + ' in ' + vehicle + ' with destination ' + str(center_id))
            
    def _deliver_packet(self, packet_id):
        with self.lock:
            self.post_service.mark_delivered({'packet_id' : packet_id})
            print(str(packet_id) + ' delivered')
        
    def _update_registered_packet(self, packet):
        # update location: distribution center
        self._transport_packet(self.center_id, 'center', packet['id'])
        # update location: transport to next distribution center
        self._transport_packet(int(packet['receiver_zip'][0]), 'car', packet['id'])
            
    def _deliver_updated_packet(self, packet):
        # update location: distribution center
        self._transport_packet(self.center_id, 'center', packet['id'])
        # update location: transport to next distribution center
        self._deliver_packet(packet['id'])
        
        
    def run(self):
        consumer = mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'packet', from_beginning=False)
        while not self.threadStop.is_set():
            for event in consumer:
                eventJson = json.loads(event.value.decode('utf-8'))
                try:
                    eventVersion = eventJson['version']
                    eventType = eventJson['type']
                    eventPayload = eventJson['payload']
                except(Exception) as e:
                    print('Event information missing.')
                    return
                try:
                    print(eventPayload['id'] + ' is consumed: event type is ' + eventType)
                except KeyError:
                    print(event)
                    
                if eventVersion != 2:
                    print('Unexpected event version (expected: 1, found: ' + str(eventVersion) + ')')
                    return
                
                if eventType == 'registered' and eventPayload['sender_zip'][0] == str(self.center_id):
                    if eventPayload['receiver_zip'][0] == str(self.center_id):
                        self._deliver_updated_packet(eventPayload)
                    else:
                        self._update_registered_packet(eventPayload)
                        print('DIST-CENTER '+str(self.center_id)+': UPDATED REGISTERED PACKET')
                    
                if eventType == 'updated_location':# and eventPayload['station'] == distributionCenter[self.center_id]['station'] and eventPayload['vehicle'] is not 'center':
                    print(eventPayload['station'], distributionCenter[self.center_id]['station'])
                    print(eventPayload['vehicle'], 'center')
                    self._deliver_updated_packet(eventPayload)
                    print('DIST-CENTER '+str(self.center_id)+': DELIVERED UPDATED PACKET')
        print('DIST-CENTER '+str(self.center_id)+' ***stopped***')

class Tester(threading.Thread):

    def __init__(self, threadStop):
        threading.Thread.__init__(self)
        self.post_service = PostService(mykafka.create_producer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092))
        self.threadStop = threadStop

    def run(self):
        packet = {'sender_name' : 'Otto Hahn',
                  'sender_street' : 'Veilchenweg 2324',
                  'sender_zip' : '12345',
                  'sender_city' : 'Hamburg',
                  'receiver_name' : 'Lise Meitner',
                  'receiver_street' : 'Amselstraße 7',
                  'receiver_zip' : '01234',
                  'receiver_city' : 'Berlin',
                  'size' : 'big',
                  'weight' : '200'}
        while not self.threadStop.is_set():
            packet_id = self.post_service.register_package(packet)
            print(str(packet_id) + ' REGISTERED')
            time.sleep(5)
        
if __name__ == '__main__':
    
    SIMULATION_TIME = 30 # Seconds
    threadStop = threading.Event()
    
    def sigint_handler(signum, frame):
        print('Interrupted')
        threadStop.set()
    
    signal.signal(signal.SIGINT, sigint_handler)
    
    threadStop.clear()
    #tester = Tester(threadStop)
    #dist = DistributionService(0, threadStop)
    threads = list()
    for i in range(2):
        threads.append(DistributionService(i, threadStop))
    threads.append(Tester(threadStop))
    
    for t in threads:
        t.daemon = True
        t.start()

    time.sleep(SIMULATION_TIME)
    threadStop.set()