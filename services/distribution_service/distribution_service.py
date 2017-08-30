import sys
import os
sys.path.append(os.path.relpath('../mykafka'))
sys.path.append(os.path.relpath('../common'))

import distribution_center
import constants
import mykafka
import threading
import json
import urllib
import urllib.request
import signal
import time

from threading import Lock

mylock = Lock()
p = print

def print(*a, **b):
	with mylock:
		p(*a, **b)
        

MAX_NUMBER = len(distribution_center.names)


class DistributionService(threading.Thread):
    
    def __init__(self, center_id, threadStop, baseurl):
        
        threading.Thread.__init__(self)
        self.center_id = center_id
        self.station = distribution_center.names[center_id]
        self.baseurl = baseurl
        self.headers = {'Content-Type':'application/json'}
        self.threadStop = threadStop
        self.lock = threading.Lock()
        
    def _zip_in_purview(self, zip_code):
        return zip_code[0] == str(self.center_id)
        
    def _transport_packet(self, center_id, vehicle, packet_id):
        time.sleep(1)
        data = {'vehicle' : vehicle, 
                'packet_id' : packet_id,
                'station' : distribution_center.names[center_id]}
    
        updateRequest = urllib.request.Request(self.baseurl + '/packet/' + packet_id +'/update',
                                               data = json.dumps(data).encode('utf8'),
                                               headers = self.headers)
        try:
            urllib.request.urlopen(updateRequest)
        except urllib.error.HTTPError as e:
            error_message = e.read()
            print(error_message)
        #print(str(packet_id) + ' in ' + vehicle + ' with destination ' + str(center_id))
        if not self.center_id:
            print('\t Transport to ' +str(center_id)+ ' with ' + vehicle + ' done.')
            
    def _deliver_packet(self, packet_id):
        time.sleep(1)
        deliverRequest = urllib.request.Request(self.baseurl + '/packet/' + packet_id +'/delivered',
                                                data=json.dumps({}).encode('utf8'),
                                                headers = self.headers)
        try:
            urllib.request.urlopen(deliverRequest)
        except urllib.error.HTTPError as e:
            error_message = e.read()
            print(error_message)
        if not self.center_id:
            print('\t Delivery done.')
        #äprint(str(packet_id) + ' delivered')
        
    def _update_registered_packet(self, packet):
        # update location: distribution center
        self._transport_packet(self.center_id, 'center', packet['packet_id'])
        # update location: transport to next distribution center
        self._transport_packet(int(packet['receiver_zip'][0]), 'car', packet['packet_id'])
            
    def _deliver_updated_packet(self, packet):
        # update location: distribution center
        self._transport_packet(self.center_id, 'center', packet['packet_id'])
        # update location: transport to next distribution center
        self._deliver_packet(packet['packet_id'])
        
        
    def run(self):
        consumer = mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'packet', from_beginning=False)
        while not self.threadStop.is_set():
            print('Starting ' + str(self.center_id))
            for event in consumer:
                time.sleep(1)
                print(str(self.center_id) + ' consumes event')
                
                eventJson = json.loads(event.value.decode('utf-8'))
                try:
                    eventVersion = eventJson['version']
                    eventType = eventJson['type']
                    eventPayload = eventJson['payload']
                    packet_id = eventPayload['packet_id']
                except(Exception) as e:
                    print('Event information missing.')
                    return
                    
                if eventVersion != 3:
                    print('Skipping event with version older than 3 (found: ' + str(eventVersion) + ')')
                    return
                
                print('-----------------')
                
                if eventType == constants.PACKET_STATE_REGISTERED and eventPayload['sender_zip'][0] == str(self.center_id):
                    if eventPayload['receiver_zip'][0] == str(self.center_id):
                        if not self.center_id:
                            print('impossible case')
                        #print(self.station + ' detected registered packet ' + packet_id[0:6] + ' and started delivery')
                        self._deliver_updated_packet(eventPayload)
                    else:
                        if not self.center_id:
                            print('Updating registered packet ' + packet_id)
                        #print(self.station + ' detected registered packet ' + packet_id[0:6] + ' and updated location')
                        self._update_registered_packet(eventPayload)
                    
                elif (eventType == constants.PACKET_STATE_UPDATE_LOCATION) and (eventPayload['station'] == self.station) and not (eventPayload['vehicle'] == 'center'):
                    if not self.center_id:
                        print('Delivering updated packet ' + packet_id)
                    #print(self.station + ' detected updated packet ' + packet_id[0:6] + ' and started delivery')
                    self._deliver_updated_packet(eventPayload)

class Tester(threading.Thread):

    def __init__(self, threadStop, baseurl, headers):
        threading.Thread.__init__(self)
        self.threadStop = threadStop
        self.baseurl = baseurl
        self.headers = headers

    def run(self):
        packet = {'sender_name' : 'Otto Hahn',
                  'sender_street' : 'Veilchenweg 2324',
                  'sender_zip' : '02345',
                  'sender_city' : 'Hamburg',
                  'receiver_name' : 'Lise Meitner',
                  'receiver_street' : 'Amselstraße 7',
                  'receiver_zip' : '11234',
                  'receiver_city' : 'Berlin',
                  'size' : 'big',
                  'weight' : '200'}
        #while not self.threadStop.is_set():
        time.sleep(1)
        for i in range(10):
            registerRequest = urllib.request.Request(self.baseurl + '/register',
                data = json.dumps(packet).encode('utf8'),
                headers = self.headers)
            response = urllib.request.urlopen(registerRequest)
            packet_id = json.loads(response.read().decode('utf8'))['packet_id']
            print(str(packet_id) + ' REGISTERED')
        #t
        
if __name__ == '__main__':
    
    post_service_url = 'http://0.0.0.0:8000'
    headers = {"Content-Type":"application/json"}
    
    SIMULATION_TIME = 10 # Seconds
    threadStop = threading.Event()
    
    #def sigint_handler(signum, frame):
    #    print('Interrupted')
    #    threadStop.set()
    
    #signal.signal(signal.SIGINT, sigint_handler)
    
    threadStop.clear()
    #tester = Tester(threadStop)
    #dist = DistributionService(0, threadStop)

    
    threads = [Tester(threadStop, post_service_url, headers)]
    for i in range(2):
        threads.append(DistributionService(i, threadStop, post_service_url))
    
    for t in threads:
        #t.daemon = True
        t.start()

    time.sleep(SIMULATION_TIME)
    threadStop.set()