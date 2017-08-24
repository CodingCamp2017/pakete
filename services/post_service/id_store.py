import post_service
import threading
import json
import sys
import os


sys.path.append(os.path.relpath('../mykafka'))
import mykafka


class IDStore:
    def __init__(self):
        self.packet_map = {}
        
    def consumeEvent(self, string):
        try:
            event = json.loads(string)
            version = event["version"]
            event_type = event["type"]
            if (version == 2 and (event_type == post_service.STATE_REGISTERED
                or event_type == post_service.STATE_UPDATE_LOCATION
                or event_type == post_service.STATE_DELIVERED)):
                    payload = event["payload"]
                    print("Read: "+string)
                    if(event_type == post_service.STATE_REGISTERED):
                        self.update(payload["id"], event_type)
                    else:
                        self.update(payload["packet_id"], event_type)
            else:
                print("Skipped")
        except json.JSONDecodeError:
            print("Skipped")
            
    def check_package_state(self, packet_id, state):
        return (packet_id in self.packet_map and state != post_service.STATE_REGISTERED) or (not packet_id in self.packet_map and state == post_service.STATE_REGISTERED)
            
        
    def update(self, packet_id, state):
        if not self.check_package_state(packet_id, state):
            print("Package "+str(packet_id)+" has not yet been registered or has been delivered")
        elif state == post_service.STATE_DELIVERED:
            del self.packet_map[packet_id]
        else:
            self.packet_map[packet_id] = state

                    
                
class IDUpdater:
    def __init__(self, idstore):
        self.idstore = idstore
        self.thread = None
        
    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        
    def run(self):
        consumer = mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, post_service.PACKET_TOPIC)
        mykafka.readFromStart(consumer, self.idstore)
        