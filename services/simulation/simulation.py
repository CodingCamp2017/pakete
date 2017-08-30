

from random import randint

import codecs
import json
import sys
import os
sys.path.append(os.path.relpath('../mykafka'))
sys.path.append(os.path.relpath('../common'))
sys.path.append(os.path.relpath('../post_service'))
import mykafka
import signal
import threading
import time
from post_service import PostService
from Exceptions import InvalidActionException

sizes = ['small','normal','big']
vehicles = ['car', 'foot', 'plane', 'rocket', 'ship', 'train', 'truck', 'center', 'failed']
fakedata = json.load(codecs.open('fakedata.json', 'r', 'utf-8-sig'))['data']

post_service = PostService(mykafka.create_producer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092))

packetList = list()
lock = threading.Lock()
threadStop = threading.Event()

def sigint_handler(signum, frame):
    print("Interrupted")
    threadStop.set()

signal.signal(signal.SIGINT, sigint_handler)

def create_random_packet():
    sender = fakedata[randint(0, len(fakedata)-1)]
    receiver = fakedata[randint(0, len(fakedata)-1)]
    packet = {}
    packet['sender_name'] = sender['name']
    packet['sender_street'] = sender['street']
    packet['sender_zip'] = str(randint(10000,99999))
    packet['sender_city'] = sender['city']
    packet['receiver_name'] = receiver['name']
    packet['receiver_street'] = receiver['street']
    packet['receiver_zip'] = str(randint(10000,99999))
    packet['receiver_city'] = receiver['city']
    packet['size'] = sizes[randint(0,2)]
    packet['weight'] = str(sender['weight'])
    return packet

def simulate_register():
    while not threadStop.is_set():
        packet = create_random_packet()
        with lock:
            packet_id = post_service.register_packet(packet)
            packetList.append(packet_id)
        #time.sleep(randint(100,2000)/1000.0)

def simulate_update():
    while not threadStop.is_set():
        if not fakedata:
            continue
        fakecity = fakedata[randint(0, len(fakedata)-1)]['city']
        vehicle = vehicles[randint(0,len(vehicles)-1)]
        with lock:
            if not packetList:
                continue
            packet_id = packetList[randint(0, len(packetList)-1)]
            try:
                post_service.update_packet_location({'packet_id':packet_id,'station':fakecity, 'vehicle':vehicle})
            except InvalidActionException as e:
                pass
        #time.sleep(randint(500,2000)/1000.0)

def simulate_deliver():
    while not threadStop.is_set():
        with lock:
            if not packetList:
                continue
            packet_id = packetList[randint(0, len(packetList)-1)]
            try:
                post_service.mark_delivered({'packet_id':packet_id})
            except InvalidActionException as e:
                pass
            packetList.remove(packet_id) 
        #time.sleep(randint(1000,4000)/1000.0)

if __name__ == '__main__':
    threadStop.clear()
    threads = list()
    threads.append(threading.Thread(target=simulate_register))
    threads.append(threading.Thread(target=simulate_update))
    threads.append(threading.Thread(target=simulate_deliver))
    
    for t in threads:
        t.start()

    for t in threads:
        t.join()