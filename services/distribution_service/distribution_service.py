import sys
import os
sys.path.append(os.path.relpath('../mykafka'))
sys.path.append(os.path.relpath('../common'))

from id_store import IDStore, IDUpdater
from constants import PACKET_TOPIC, PACKET_STATE_REGISTERED, PACKET_STATE_UPDATE_LOCATION, PACKET_EVENT_VERSION, PACKET_STATE_DELIVERED
import distribution_center
import mykafka

import threading
import json
import urllib
import urllib.request
import time

MAX_NUMBER = len(distribution_center.names)

def addPredicate(event_type, payload):
    return event_type == PACKET_STATE_REGISTERED and payload['auto_deliver']

def deletePredicate(event_type, payload, current_state):
    return event_type == PACKET_STATE_DELIVERED
    
storeTransform = lambda eventtype, old, payload: {'receiver_zip' : payload['receiver_zip']}

idstore = IDStore(PACKET_EVENT_VERSION, addPredicate, deletePredicate, storeTransform, verbose=False)
updater = IDUpdater(idstore, from_beginning=False)
updater.start()


class DistributionService(threading.Thread):
    
    def __init__(self, center_id, idstore, baseurl, threadStop):
        
        threading.Thread.__init__(self)
        self.center_id = center_id
        self.station = distribution_center.names[center_id]
        self.baseurl = baseurl
        self.headers = {'Content-Type':'application/json'}
        self.threadStop = threadStop
        self.lock = threading.Lock()
        self.idstore = idstore
        self.updater = IDUpdater(self.idstore)
        
    def _this_is_a_register_event_i_need_to_handle(self, event_type, payload):
        return ((event_type == PACKET_STATE_REGISTERED) and 
                (payload['receiver_zip'][0] == str(self.center_id)) and
                payload['auto_deliver'])
    
    def _this_is_an_update_event_i_need_to_handle(self, event_type, payload):
        return (event_type == PACKET_STATE_UPDATE_LOCATION and
                payload['station'] == self.station and
                not (payload['vehicle'] == 'center') and
                self.idstore.packet_in_store['packet_id'])
        
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
        print(str(packet_id) + ' in ' + vehicle + ' from ' + str(self.center_id) + ' to ' + str(center_id))
            
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
        print(str(packet_id) + ' delivered from ' + str(self.center_id))
        
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
        consumer = mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, PACKET_TOPIC, from_beginning=False)
        time.sleep(1)
        while not self.threadStop.is_set():
            print('Starting ' + str(self.center_id))
            for event in consumer:
                #time.sleep(1)
                #print(str(self.center_id) + ' consumes event')
                
                eventJson = json.loads(event.value.decode('utf-8'))
                try:
                    eventVersion = eventJson['version']
                    eventType = eventJson['type']
                    eventPayload = eventJson['payload']
                except(Exception) as e:
                    print('Event information missing.')
                    return
                    
                if eventVersion != 3:
                    print('Skipping event with version older than 3 (found: ' + str(eventVersion) + ')')
                    return
                
                #print('-----------------')
                
                if self._this_is_a_register_event_i_need_to_handle(eventType, eventPayload):
                    if eventPayload['receiver_zip'][0] == str(self.center_id):
                        self._deliver_updated_packet(eventPayload)
                    else:
                        self._update_registered_packet(eventPayload)
                    
                elif self._this_is_an_update_event_i_need_to_handle(eventType, eventPayload):
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
        for i in range(10):
            time.sleep(1)
            registerRequest = urllib.request.Request(self.baseurl + '/register',
                data = json.dumps(packet).encode('utf8'),
                headers = self.headers)
            response = urllib.request.urlopen(registerRequest)
            packet_id = json.loads(response.read().decode('utf8'))['packet_id']
            print(str(packet_id) + ' REGISTERED')
        #t
        
if __name__ == '__main__':
    
    post_service_url = 'http://0.0.0.0:43747'
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