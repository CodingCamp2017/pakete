# -*- coding: utf-8 -*-

import sys
import os
import datetime
sys.path.append(os.path.relpath('../mykafka'))

import mykafka
import json
import model
import threading
import pandas as pd
import numpy as np

import time
class Filter:
    __start = 0
    __end = -1
    def __init__(self,start = 0,end=-1):
        self.__start = int(start)
        self.__end = int(end)

    def accept(self, time):
        time = int(time)
        if(self.__end == -1):
            return True
        return self.__start <= time and self.__end >= time
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

            self.packets = model.Model()

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
                
            if eventVersion !=3:
                #print('Unexpected event version (expected: 1, found: ' + str(eventVersion) + ')')
                return
        
            #print(self.packets)
            if eventType == "registered":
                supModel = model.Model({ "register_time" : eventTime,
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
                             })
                if("packet_id" in eventPayload):# Version 3
                    self.packets.set(eventPayload["packet_id"],supModel)
                else:# Version2
                    self.packets.set(eventPayload["id"], supModel)
                #print(eventPayload)
            elif eventType == "updated_location":
                self.packets.get(eventPayload["packet_id"]).append("stations",{"station_time" : eventTime,
                                                                               "station_name" : eventPayload["station"],
                                                                               "vehicle" : eventPayload["vehicle"]})
                #print(eventPayload)
            elif eventType == "delivered":
                # DEBUG REMOVE IF STATEMENT!
                if self.packets.has(eventPayload["packet_id"]):
                    self.packets.get(eventPayload["packet_id"]).set("delivery_time",eventTime)
                #print(eventPayload)
                #else:
                #print(eventPayload)

            else:
                print("Unknown eventType: " + eventType)
#Summe aller Pakete
        def getPacketCount(self):
            return self.packets.size()

        def getAverageDeliveryTime(self,filter = Filter()):
            timesum = 0
            delivered_count = 0

            for packet_id, packet_data in self.packets.items(filter):
                if packet_data.has("delivery_time"):
                    timesum += int(packet_data.get("delivery_time")) - int(packet_data.get("register_time"))
                    delivered_count += 1

            if delivered_count == 0:
                return 0

            return timesum*1.0 / delivered_count
        def getAverageDeliveryTimeByTime(self,timefilter,filter = Filter()):
            values = {}
            for packet_id, packet_data in self.packets.items(filter):
                if packet_data.has("delivery_time"):
                    timestamp = packet_data.getDate(timefilter)
                    self.__addSumDataSet("summe", str(int(packet_data.get("delivery_time")) - int(packet_data.get("register_time"))), 'count', values, timestamp)
            return self.__calcArvages("summe", 'count', values)

        def getAverageWeightByTime(self,timefilter,filter = Filter()):
            values = {}
            for packet_id, packet_data in self.packets.items(filter):
                    timestamp = packet_data.getDate(timefilter)
                    self.__addSumDataSet("summe", str(float(packet_data.get("weight"))), 'count', values, timestamp)
            return self.__calcArvages("summe", 'count', values)


        def getAverageStationCount(self,filter = Filter()):
            delivered_count = 0
            stationcount = 0
            for packet_id, packet_data in self.packets.items(filter):
                stationcount += len(packet_data.get("stations"))
                if packet_data.has("delivery_time"):
                    delivered_count += 1

            if stationcount == 0:
                return 0

            return self.getPacketCount() /stationcount*1.0


        def ByTime(self,timefilter,filter = Filter()):
            values = {}

            for packet_id, packet_data in self.packets.items(filter):
                timestamp = packet_data.getDate(timefilter)
                self.__addSumDataSet("summe",packet_data.get("weight"),'count',values,timestamp)
            return self.__calcArvages("summe",'count',values)

        def __addSumDataSet(self,key1,value1,key2,values,timestamp):
            if timestamp not in values:
                values[timestamp] = {key1: float(value1), "count": 1}
            else:
                values[timestamp][key1] += float(value1)
                values[timestamp][key2] += 1
        def __calcArvages(self,key1,key2,values):
            answer = {}
            for timeframe in values:
                answer[timeframe] = float(values[timeframe][key1]) / values[timeframe][key2]
                values[timeframe]["average"] = answer[timeframe]
            return  answer



# Git die Anzahl des Values die in diesem Key zurück
        def getCountOfKeyValue(self,key,value,filter = Filter()):
            keycout = 0
            for packet_id, packet_data in self.packets.items(filter):
                if packet_data.get(key) == value:
                    keycout +=1
            return keycout;
        # end of FKT

        def getCountOfKeyValueByTime(self,key,value,timefilter,filter = Filter()):
            values = {}
            for packet_id, packet_data in self.packets.items(filter):
                if packet_data.get(key) == value:
                    timestamp = packet_data.getDate(timefilter)
                    if timestamp not in values:
                        values[timestamp] = 1
                    else:
                        values[timestamp] += 1

            return values;
        # end of FKT
# Git die Anzahl von gleichen Values für einen Key zurück
        def getCountOfKey(self, key,filter = Filter()):
            values = {}
            for packet_id, packet_data in self.packets.items(filter):
                if packet_data.get(key) not in values:
                    values[packet_data.get(key)] = 1
                else:
                    values[packet_data.get(key)] += 1
            return values;
            # end of FKT

        def getCountOfKeyByTime(self, key, timefilter,filter = Filter()):
            values = {}
            for packet_id, packet_data in self.packets.items(filter):
                timestamp = packet_data.getDate(timefilter)
                value = packet_data.get(key);
                if timestamp not in values:
                    values[timestamp] = {}
                if(value not in values[timestamp]):
                    values[timestamp][value] = 1
                else:
                    values[timestamp][value] += 1

            return values;
           # end of FKT

        def getCountOfRegistrationByTime(self,timefilter,filter = Filter()):
            values = {}
            for packet_id, packet_data in self.packets.items(filter):
                timestamp = packet_data.getDate(timefilter)
                if timestamp not in values:
                    values[timestamp] = 1
                else:
                    values[timestamp] +=1

            return values;
        # end of FKT
        def getCountOfDeliveredByTime(self, timefilter):
            values = {}
            for packet_id, packet_data in self.packets.items():
                if packet_data.has('delivery_time'):
                    timestamp = self._getDate(packet_data.get('delivery_time'), timefilter)
                    if timestamp not in values:
                        values[timestamp] = 1
                    else:
                        values[timestamp] += 1
            return values;
        # end of FKT
        def getCountOfCurrendLocationOfPackets(self,ByName=False,filter = Filter()):
            if ByName:
                name = 'station_name'
            else:
                name = 'vehicle'
            values = {'registert':0, 'delivery' : 0}
            for packet_id, packet_data in self.packets.items(filter):
                if packet_data.has('delivery_time'):
                    values['delivery']  +=1;
                elif len(packet_data.get('stations')) == 0:
                    values['registert'] +=1;
                else:
                    vehicle = packet_data.get('stations')[-1][name]
                    if vehicle not in values:
                        values[vehicle] = 1
                    else:
                        values[vehicle] +=1;
            if(values['registert'] == 0):
                values['registert'] = None
            if (values['delivery'] == 0):
                values['delivery'] = None
            return values;
        # end of FKT

        def getCountOfLacationByTime(self, timefilter,ByName=False,onlyCurrentLocation=True,onlyUndeliveryed = False,filter = Filter()):
            if ByName:
                name = 'station_name'
            else:
                name = 'vehicle'

            values = {}
            for packet_id, packet_data in self.packets.items(filter):

                if (onlyUndeliveryed and packet_data.has('delivery_time')):
                    continue
                elif (onlyUndeliveryed and packet_data.has('delivery')):
                    self.__coutUP(self._getDate(packet_data.get('delivery_time'),timefilter), values, 'registert')
                elif len(packet_data.get('stations')) == 0:
                    self.__coutUP(packet_data.getDate(timefilter),values,'registert')
                elif onlyCurrentLocation:
                    self._getCountOfLacationByTimeSubroutine(-1,values,timefilter,packet_data,name)
                else:
                    for x in range(0,len(packet_data.get('stations')) ):
                        self._getCountOfLacationByTimeSubroutine(x, values, timefilter, packet_data, name)
            return values;
        # end of FKT
        def _getCountOfLacationByTimeSubroutine(self,id,values,timefilter,packet_data,name):
            timestamp = self._getDate(packet_data.get('stations')[id]['station_time'],timefilter)
            vehicle = packet_data.get('stations')[id][name]
            self.__coutUP(timestamp,values,vehicle)
            return

        def __coutUP(self,timestamp,values,key):
            if timestamp not in values:
                values[timestamp] = {}
            if key not in values[timestamp]:
                values.get(timestamp)[key] = 1;
            else:
                values.get(timestamp)[key] += 1;
            return
        # end of FKT





        def _getDate(self,UNIXTime,timefilter):
            return datetime.datetime.fromtimestamp(int(UNIXTime)).strftime(timefilter)

        def getTimespentIn(self,ByName=False,filter = Filter()):
            if ByName:
                name = 'station_name'
            else:
                name = 'vehicle'
            values = {}
            counts = {}
            for packet_id, packet_data in self.packets.items(filter):
                start = int(packet_data.get('register_time'))

                list = packet_data.get('stations')
                for i in range(len(list)):
                    currendstation = packet_data.get('stations')[i]
                    ziel = int(currendstation['station_time'])
                    key = currendstation[name]
                    if not key in values:
                        values[key] = 0
                        counts[key] = 0
                    values[key] += ziel-start
                    counts[key] +=1
                    start = ziel
                if packet_data.has('delivery_time'):
                    ziel = int(packet_data.get('delivery_time'))

                    if not 'delivery' in values:
                        values['delivery'] = 0
                        counts['delivery'] = 0
                    values['delivery'] += ziel - start
                    counts['delivery'] += 1

                out = {}
                for key,value in values.items():
                    out[key] = values[key]/counts[key]
            return out;
        # end of FKT
        def getTimespentInByTime(self,timefilter,ByName=False,filter = Filter()):
            if ByName:
                name = 'station_name'
            else:
                name = 'vehicle'
            values = {}
            for packet_id, packet_data in self.packets.items(filter):
                start = int(packet_data.get('register_time'))
                timestamp = packet_data.getDate(timefilter)
                list = packet_data.get('stations')
                for i in range(len(list)):
                    currendstation = packet_data.get('stations')[i]
                    ziel = int(currendstation['station_time'])
                    key = currendstation[name]
                    if not timestamp in values:
                        values[timestamp] = {'values' : {} , 'counts' : {}}

                    if not key in values[timestamp]['values']:
                        values[timestamp]['values'][key] = 0
                        values[timestamp]['counts'][key] = 0

                    values[timestamp]['values'][key] += ziel-start
                    values[timestamp]['counts'][key] += 1
                    start = ziel
                    timestamp = self._getDate(ziel, timefilter)
                if packet_data.has('delivery_time'):
                    ziel = int(packet_data.get('delivery_time'))
                    if not timestamp in values:
                        values[timestamp] = {'values' : {} , 'counts' : {}}

                    if not 'delivery' in values[timestamp]['values']:
                        values[timestamp]['values']['delivery'] = 0
                        values[timestamp]['counts']['delivery'] = 0

                    values[timestamp]['values']['delivery'] += ziel - start
                    values[timestamp]['counts']['delivery'] += 1

                out = {}
                for time in values:
                    tmp = {}
                    for key,value in values[time]['values'].items():
                        tmp[key] = values[time]['values'][key]/values[time]['counts'][key]
                    out[time] = tmp
            return out;
        # end of FKT
if __name__ == "__main__":
    consumer = mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'packet')
    srv = WarehouseService(consumer)

    while(True):
        time.sleep(3)
        print("Anzahl Pakete: " + str(srv.getPacketCount()))

        ##Gesamte druchschnittleiche Laufzeit
        #print("Lieferzeit: " + str(srv.getAverageDeliveryTime()))
        #print("Lieferzeit: " + str(srv.getAverageDeliveryTime(Filter(251436848146384814614364168416,251436848146384814614364168416))))

        ##druchschnittliche Laufzeit TODO
        #print("Lieferzeit: " + str(srv.getAverageDeliveryTimeByTime('%Y-%m-%d %H')))
        #print("Lieferzeit: " + str(srv.getAverageDeliveryTimeByTime('%Y-%m-%d')))

        ##druchschnittliches Gewicht auf Zeit TODO'''
        print("Gewicht: " + str(srv.getAverageWeightByTime("%Y-%m-%d %H")))
'''
        ##Data of Values TODO Number TODO Text
        #print("Anzahl Sender_name "+str(srv.getCountOfKey("sender_name")))
        #print("Anzahl Sender_name nach Zeit: " + str(srv.getCountOfKeyByTime("sender_name", '%Y-%m-%d %H')))
        #print("Anzahl sender_city "+str(srv.getCountOfKey("sender_city")))
        print("Anzahl sender_city "+str(srv.getCountOfKey("size")))

        ##Current Location of Packs TODO
        #print(srv.getCountOfCurrendLocationOfPackets())
        #rint(srv.getCountOfCurrendLocationOfPackets(True))

        ##Location by Time TODO
        #print(srv.getCountOfLacationByTime('%w'))
        #print(srv.getCountOfLacationByTime('%Y-%m-%d %H'))
        #print(srv.getCountOfLacationByTime('%Y-%m-%d'))
        #print(srv.getCountOfLacationByTime('%Y-%m-%d',False,False))
        #print(srv.getCountOfLacationByTime('%Y-%m-%d',False,False,False))
        #print(srv.getCountOfLacationByTime('%Y-%m-%d',False,True,False))
        #print(srv.getCountOfLacationByTime('%Y-%m-%d', True))
        #print(srv.getCountOfLacationByTime('%Y-%m-%d', True, False))
        #print(srv.getCountOfLacationByTime('%Y-%m-%d', True, False, False))
        #print(srv.getCountOfLacationByTime('%Y-%m-%d', True, True, False))
        #print("Anzahl Sender_name von Otto Hahn: " + str(srv.getCountOfKeyValue("sender_name", "Otto Hahn")))
        #print("Anzahl Sender_name von Otto Hahn: " + str(srv.getCountOfKeyValueByTime("sender_name", "Otto Hahn", '%Y-%m-%d %H')))
        #print("Anzahl Sender_name nach Zeit: " + str(srv.getCountOfKeyByTime("sender_name", '%Y-%m-%d %H')))#

        ##Registration TODO
        #print(srv.getCountOfRegistrationByTime("%Y-%m-%d %H"))
        #print(srv.getCountOfDeliveredByTime("%Y-%m-%d %H"))

        print(srv.getTimespentInByTime("%Y-%m-%d %H"))
        print(srv.getTimespentInByTime("%Y-%m-%d %H",True))
        print(srv.getTimespentInByTime("%w"))
    '''



