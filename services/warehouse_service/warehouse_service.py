# -*- coding: utf-8 -*-

import sys
import os
import datetime
from datetime import date
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
class WarehouseService:        
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
        
            #print(self.packets)
            if eventType == "registered":
                self.packets[eventPayload["id"]] = { "register_time" : eventTime,
                                                     "stations" : [],
                                                     "size": eventPayload['size'],
                                                     "weight": eventPayload['weight'],
                                                     "sender_name": eventPayload['sender_name'],
                                                     "sender_street": eventPayload['sender_street'],
                                                     "sender_zip": eventPayload['sender_zip'],
                                                     "sender_city": eventPayload['sender_city'],
                                                     "receiver_name": eventPayload['receiver_name'],
                                                     "receiver_street": eventPayload['receiver_street'],
                                                     "receiver_zip": eventPayload['receiver_zip'],
                                                     "receiver_city": eventPayload['receiver_city']
                                                     }
                #print(eventPayload)
            elif eventType == "updated_location":
                self.packets[eventPayload["packet_id"]]["stations"].append({"station_time" : eventTime,
                                                                            "station_name" : eventPayload["station"],
                                                                            "vehicle" : eventPayload["vehicle"]})
                #print(eventPayload)
            elif eventType == "delivered":
                self.packets[eventPayload["packet_id"]]["delivery_time"] = eventTime
                #print(eventPayload)
            else:
                print("Unknown eventType: " + eventType)

        def getPacketCount(self):
            return len(self.packets)
        def getPacketCountByTime(self,timestamp):
            return self.getListbyRegistrationDay(timestamp);


        def getAverageDeliveryTime(self):
            timesum = 0
            delivered_count = 0
            stationcount = 0
            for packet_id, packet_data in self.packets.items():
                stationcount += len(packet_data["stations"])
                if "delivery_time" in packet_data:
                    timesum += int(packet_data["delivery_time"]) - int(packet_data["register_time"])
                    delivered_count += 1

            return (timesum*1.0 / delivered_count, self.getPacketCount() /stationcount*1.0)
        def getAverageWeight(self):
            delivered_count = 0
            summWeight = 0
            for packet_id, packet_data in self.packets.items():
                summWeight += float(packet_data["weight"])
                if "delivery_time" in packet_data:
                    delivered_count += 1

            return summWeight/ delivered_count;

        def getListOfKey(self,key):
            values = {}
            for packet_id, packet_data in self.packets.items():
                if packet_data[key] not in values:
                    values[packet_data[key]] = 1
                else:
                    values[packet_data[key]] +=1

            return values;
        # end of FKT

        def getCountOfKeyValue(self,key,value):
            keycout = 0
            for packet_id, packet_data in self.packets.items():
                if packet_data[key] == value:
                    keycout +=1
            return keycout;
        # end of FKT
        def getCountOfKeyValueByTime(self,key,value,timefilter):
            values = {}
            for packet_id, packet_data in self.packets.items():
                if packet_data[key] == value:
                    timestamp = self._getDate(packet_data['register_time'], timefilter)
                    if timestamp not in values:
                        values[timestamp] = 1
                    else:
                        values[timestamp] += 1

            return values;

        # end of FKT
        def getCountOfKeyByTime(self, key, timefilter):
            values = {}
            for packet_id, packet_data in self.packets.items():
                timestamp = self._getDate(packet_data['register_time'], timefilter)
                value = packet_data[key];
                if timestamp not in values:
                    values[timestamp] = {}
                if(value not in values[timestamp]):
                    values[timestamp][value] = 1
                else:
                    values[timestamp][value] += 1

            return values;
           # end of FKT

        def getListbyRegistrationDay(self,timefilter):
            values = {}
            for packet_id, packet_data in self.packets.items():
                timestamp = self._getDate(packet_data['register_time'],timefilter)
                if timestamp not in values:
                    values[timestamp] = 1
                else:
                    values[timestamp] +=1

            return values;
        # end of FKT
        def getListbyDeliveredDay(self, timefilter):
            values = {}
            for packet_id, packet_data in self.packets.items():
                if 'delivery_time' in packet_data:
                    timestamp = self._getDate(packet_data['delivery_time'], timefilter)
                    if timestamp not in values:
                        values[timestamp] = 1
                    else:
                        values[timestamp] += 1
            return values;
        # end of FKT

        def getListbyLacationDay(self, timefilter,ByName=False,onlyCurrentLocation=True,onlyUndeliveryed = True):
            if ByName:
                name = 'station_name'
            else:
                name = 'vehicle'

            values = {}
            for packet_id, packet_data in self.packets.items():

                if ('delivery_time' in packet_data) & onlyUndeliveryed:
                    continue
                elif len(packet_data['stations']) == 0:
                    continue
                elif onlyCurrentLocation:
                    self._getListbyLacationDaySubroutine(-1,values,timefilter,packet_data,name)
                else:
                    for x in range(0,len(packet_data['stations']) ):
                        self._getListbyLacationDaySubroutine(x, values, timefilter, packet_data, name)
            return values;
        # end of FKT
        def _getListbyLacationDaySubroutine(self,id,values,timefilter,packet_data,name):
            timestamp = self._getDate(packet_data['stations'][id]['station_time'],timefilter)
            vehicle = packet_data['stations'][id][name]
            if timestamp not in values:
                values[timestamp] = {}
            if vehicle not in values[timestamp]:
                values[timestamp][vehicle] = 1;
            else:
                values[timestamp][vehicle] += 1;
            return
            # end of FKT
        def _getDate(self,UNIXTime,timefilter):
            return datetime.datetime.fromtimestamp(int(UNIXTime)).strftime(timefilter)
        def getListOfCurrendLocationOfPackets(self,ByName=False):
            if ByName:
                name = 'station_name'
            else:
                name = 'vehicle'
            values = {'registert':0, 'delivery' : 0}
            for packet_id, packet_data in self.packets.items():
                if 'delivery_time' in packet_data:
                    values['delivery']  +=1;
                elif len(packet_data['stations']) == 0:
                    values['registert'] +=1;
                else:
                    vehicle = packet_data['stations'][-1][name]
                    if vehicle not in values:
                        values[vehicle] = 1
                    else:
                        values[vehicle] +=1;
            return values;
        # end of FKT


if __name__ == "__main__":
    consumer = mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'packet')
    srv = WarehouseService(consumer)

    time.sleep(5)
    '''print("Anzahl Pakete: " + str(srv.getPacketCount()))
print("Lieferzeit: " + str(srv.getAverageDeliveryTime()))
print("Gewicht " + str(srv.getAverageWeight()))
print("Anzahl Sender_name von Otto Hahn: "+str(srv.getCountOfKeyValue("sender_name","Otto Hahn")))
print("Anzahl Sender_name von Otto Hahn: "+str(srv.getCountOfKeyValueByTime("sender_name","Otto Hahn",'%Y-%m-%d %H:%M')))
print("Anzahl Sender_name nach Zeit: " + str(srv.getCountOfKeyByTime("sender_name", '%Y-%m-%d %H')))
print("Anzahl Sender_name "+str(srv.getListOfKey("sender_name")))
print("Anzahl sender_city "+str(srv.getListOfKey("sender_city")))'''
    print(srv.getListbyRegistrationDay('%Y-%m-%d'))
    print(srv.getListbyRegistrationDay('%w'))
    print(srv.getListbyRegistrationDay('%Y-%m-%d %H'))
    '''
    print(srv.getListbyDeliveredDay('%Y-%m-%d %H'))
    print(srv.getListOfCurrendLocationOfPackets())
    print(srv.getListOfCurrendLocationOfPackets(True))
    print(srv.getListbyLacationDay('%Y-%m-%d'))
    print(srv.getListbyLacationDay('%Y-%m-%d',False,False))
    print(srv.getListbyLacationDay('%Y-%m-%d',False,False,False))
    print(srv.getListbyLacationDay('%Y-%m-%d',False,True,False))
    print(srv.getListbyLacationDay('%Y-%m-%d', True))
    print(srv.getListbyLacationDay('%Y-%m-%d', True, False))
    print(srv.getListbyLacationDay('%Y-%m-%d', True, False, False))
    print(srv.getListbyLacationDay('%Y-%m-%d', True, True, False))'''