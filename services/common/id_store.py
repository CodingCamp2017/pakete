import threading
import json
import sys
import os


sys.path.append(os.path.relpath('../mykafka'))
import mykafka

from constants import PACKET_TOPIC, PACKET_STATE_REGISTERED, PACKET_STATE_UPDATE_LOCATION, PACKET_STATE_DELIVERED

'''
Stores packet_ids of all packets that are currently in the delivery chain 
(registered but not yet delivered).
'''
class IDStore:
    def __init__(self, version, addPredicate, deletePredicate, storeTransform = lambda eventtype, old, payload:None, verbose=False):
        self.packet_map = {}#dict packet_id -> (state, storeTransform(payload))
        self.version = version
        self.addPred = addPredicate
        self.deletePred = deletePredicate
        self.storeTransform = storeTransform
        self.verbose = verbose
    
    '''
    Implemented to be used with mykafka.readFromStart.
    Parses each event on the packet topic. If the event is related to register/update/deliver
    process, the packet_map is updated.
    '''
    def consumeEvent(self, string):
        try:
            event = json.loads(string)
            version = event["version"]
            event_type = event["type"]
            if (version == self.version):
                    payload = event["payload"]
                    if self.verbose:
                        print("Read: "+string)
                    packet_id = payload['packet_id']
                    if packet_id in self.packet_map:
                        self._update_packet(packet_id, event_type, payload)
                    else:
                        self._add_packet(packet_id, event_type, payload)
            elif self.verbose:
                print("Skipped")
        except json.JSONDecodeError:
            print("Skipped")

    def _add_packet(self, packet_id, event_type, payload):
        if self.addPred(event_type, payload):
            if self.verbose:
                print("Added packet "+packet_id)
            self.packet_map[packet_id] = (event_type, self.storeTransform(event_type, None, payload))

    def _update_packet(self, packet_id, event_type, payload):
        current_state, data = self.packet_map[packet_id]
        if self.deletePred(event_type, payload, current_state):
            if self.verbose:
                print("Removed packet "+packet_id)
            del self.packet_map[packet_id]
        else:
            if self.verbose:
                print("Updated packet "+packet_id+" from "+current_state+" to "+event_type)
            self.packet_map[packet_id] = (event_type, self.storeTransform(event_type, data, payload))
    '''
    Returns true if the packet with the given packet_id is in the delivery chain
    '''
    def packet_in_store(self, packet_id):
        return packet_id in self.packet_map

    def get_data_for_packet(self, packet_id):
        if packet_id in self.packet_map:
            state, data = self.packet_map[packet_id]
            return data
        else:
            return None
'''
Consumer that reads the packet topic and updates IDStore
'''
class IDUpdater:
    def __init__(self, idstore):
        self.idstore = idstore
        self.thread = None
        
    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        
    def run(self):
        consumer = mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, PACKET_TOPIC)
        mykafka.readFromStart(consumer, self.idstore)
        
