# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.relpath('../mykafka'))

import mykafka
import json
import threading

import pandas as pd
import numpy as np

import time

'''
This consumer listens to the topic packet and builds the internal packet history
model.
'''
class TrackingService:        
        '''
        consumer: A consumer listening to the topic packet
        '''
        def __init__(self, consumer):
            self.consumer = consumer
            self.consumerThread = None           

            self.packets = {}

            self.readPackets()

        '''
        start consuming the whole kafka log to create packet model
        '''
        def readPackets(self):
            print('Starting packet reading...')
            
            if  self.consumerThread is None:
                self.consumerThread = threading.Thread(target=self.startConsuming)
                self.consumerThread.start()
                return "Consumer started and reading packets."
            else:
                return "Consumer already running."
             
        def startConsuming(self):
            mykafka.readFromStart(self.consumer, self)
        
        '''
        Implemented for mykafka.readFromStart
        '''
        def consumeEvent(self, event):
            eventJson = json.loads(event)  
            
            try:
                eventVersion = eventJson['version']
                eventType = eventJson['type']
                eventTime = eventJson['time']
                eventPayload = eventJson['payload']

            except(Exception) as e:
                print('Event information missing.')
                return
                
            if eventVersion != 2:
                print('Unexpected event version (expected: 1, found: ' + str(eventVersion) + ')')
                return
        
            print(self.packets)

            if eventType == "registered":
                self.packets[eventPayload["id"]] = { "register_time" : eventTime, "stations" : []}
            elif eventType == "updated_location":                
                self.packets[eventPayload["packet_id"]]["stations"].append({"station_time" : eventTime, 
                                                                            "station_name" : eventPayload["station"], 
                                                                            "vehicle" : eventPayload["vehicle"]})
            elif eventType == "delivered":
                self.packets[eventPayload["packet_id"]]["delivery_time"] = eventTime
            else:
                print("Unknown eventType: " + eventType)

        def getPacketCount(self):
            return len(self.packets)

        def getAverageDeliveryTime(self):
            timesum = 0
            delivered_count = 0
            stationcount = 0
            for packet_id, packet_data in self.packets.items():                
                stationcount += len(packet_data["stations"])
                if "delivery_time" in packet_data:
                    timesum += int(packet_data["delivery_time"]) - int(packet_data["register_time"])
                    delivered_count += 1

            return (timesum*1.0 / delivered_count, stationcount*1.0 / self.getPacketCount())




if __name__ == "__main__":
    consumer = mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'packet')
    srv = TrackingService(consumer)

    time.sleep(3)
    print(srv.getPacketCount())
    print(srv.getAverageDeliveryTime())