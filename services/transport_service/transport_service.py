import sys
import os
sys.path.append(os.path.relpath('../mykafka'))

import mykafka
import threading
import json
import urllib

paketzentren = {0 : {'name' : 'Brief Leipzig', 'address' : '04158 Leipzig,Poststr. 28'},
                1 : {'name' : 'Brief Neubrandenburg', 'address' : '17235 Neustrelitz,Bürgerseeweg 27'},
                2 : {'name' : 'Brief Hamburg-Süd', 'address' : '21035 Hamburg,Rungedamm 37'},
                3 : {'name' : 'Brief Kassel', 'address' : '34355 Staufenberg,Im Rotte 2'},
                4 : {'name' : 'Brief Essen', 'address' : '46282 Dorsten,Lünsingskuhle 70'},
                5 : {'name' : 'Brief Koblenz', 'address' : '56566 Neuwied,Rostocker Str. 14'},
                6 : {'name' : 'Paketzentrum Obertshausen', 'address' : '63179 Obertshausen,Im Birkengrund'},
                7 : {'name' : 'Brief Reutlingen', 'address' : '72184 Eutingen im Gäu, Am Flugplatz 14'},
                8 : {'name' : 'Brief Augsburg', 'address' : '86154 Augsburg,Stuttgarter Str. 33'},
                9 : {'name' : 'Brief Nürnberg', 'address' : '90475 Nürnberg,Am Tower 10'}}


class DistributionService(threading.Thread):
    
    def __init__(self, service_id):
        threading.Thread.__init__(self)
        self.service_id = service_id
        self.name = paketzentren[service_id]['name']
        self.baseurl = baseurl
        self.headers = headers
        self.lock = threading.Lock()
        
    def _zip_in_purview(self, zip_code):
        return zip_code[0] == str(self.service_id)
        
    def _transport_packet(self, station, vehicle, packet_id, mode):
        data = {'station' : station,
                'vehicle' : vehicle,
                'packet_id' : packet_id}
        with self.lock:
            updateRequest = urllib.request.Request(self.baseurl + 'packet/' + packet_id + '/update',
                                                   data = json.dumps(data).encode('utf8'),
                                                   headers = self.headers)
            urllib.request.urlopen(updateRequest)
            
    def _deliver_packet(self, packet_id):
        with self.lock:
            deliverRequest = urllib.request.Request(self.baseurl + 'packet/' + packet_id + '/delivered',
                                                    data=json.dumps({}).encode('utf8'),
                                                    headers = self.headers)
            urllib.request.urlopen(deliverRequest)
        
    def _update_registered_packet(self, packet):
        # update location: distribution center
        self._transport_packet(self.name, 'center', packet['id'])
        # update location: transport to next distribution center
        self._transport_packet(paketzentren[packet['receiver_zip'][0]]['name'], 'car', packet['id'])
            
    def _deliver_updated_packet(self, packet):
        # update location: distribution center
        self._transport_packet(self.name, 'center', packet['id'])
        # update location: transport to next distribution center
        self._deliver_packet(packet['id'])
        
        
    def run(self):
        consumer = mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'packet', from_beginning=False)
        for event in consumer:
            eventJson = json.loads(event.value.decode('utf-8'))
            try:
                eventVersion = eventJson['version']
                eventType = eventJson['type']
                eventPayload = eventJson['payload']
            except(Exception) as e:
                print('Event information missing.')
                return
                
            if eventVersion != 2:
                print('Unexpected event version (expected: 1, found: ' + str(eventVersion) + ')')
                return
                
            if eventType == 'registered' and eventPayload['sender_zip'][0] == str(self.service_id):
                if eventPayload['receiver_zip'][0] == str(self.service_id):
                    self._deliver_updated_packet(eventPayload)
                else:
                    self._update_registered_packet(eventPayload)
                
            if eventType == 'updated_location' and eventPayload['receiver_zip'][0] == str(self.service_id) and eventPayload['vehicle'] is not 'center':
                self._deliver_updated_packet(eventPayload)


if __name__ == '__main__':
    
    threads = list()
    for i in range(2):
        threads.append(DistributionService(i))
    
    for t in threads:
        t.daemon = True
        t.start()
