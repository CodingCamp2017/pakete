import threading
import json
import sys
import os


sys.path.append(os.path.relpath('../mykafka'))
sys.path.append(os.path.relpath('../common'))
import mykafka

from constants import PACKET_TOPIC, PACKET_STATE_REGISTERED, PACKET_STATE_UPDATE_LOCATION, PACKET_STATE_DELIVERED

'''
Stores packet_ids of all packets that are currently in the delivery chain 
(registered but not yet delivered).
'''
class IDStore:
    def __init__(self, verbose=False):
        self.packet_map = {}
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
            if (version == 2 and (event_type == PACKET_STATE_REGISTERED
                or event_type == PACKET_STATE_UPDATE_LOCATION
                or event_type == PACKET_STATE_DELIVERED)):
                    payload = event["payload"]
                    if self.verbose:
                        print("Read: "+string)
                    if(event_type == PACKET_STATE_REGISTERED):
                        self.update(payload["id"], event_type)
                    else:
                        self.update(payload["packet_id"], event_type)
            elif self.verbose:
                print("Skipped")
        except json.JSONDecodeError:
            print("Skipped")
            
    '''
    Returns true if the packet with the given id can be updated with the given state
    '''
    def check_package_state(self, packet_id, state):
        return (packet_id in self.packet_map and state != PACKET_STATE_REGISTERED) or (not packet_id in self.packet_map and state == PACKET_STATE_REGISTERED)
            
    '''
    Returns true if the packet with the given id is in the delivery chain
    '''
    def packet_in_store(self, packet_id):
        return packet_id in self.packet_map
            
    '''
    Updates the packet_map. If the state is register the packet will be added to the map.
    If the state is update, its state will be updated, if the state is delivered, the packet will be deleted from the packet_map
    '''
    def update(self, packet_id, state):
        if not self.check_package_state(packet_id, state):
            print("Package "+str(packet_id)+" has not yet been registered or has been delivered")
        elif state == PACKET_STATE_DELIVERED:
            del self.packet_map[packet_id]
        else:
            self.packet_map[packet_id] = state

                    
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
        