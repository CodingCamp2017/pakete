# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.relpath('../mykafka'))
sys.path.append(os.path.relpath('../common'))

import mykafka
from constants import PACKET_TOPIC, PACKET_EVENT_VERSION, PACKET_STATE_REGISTERED, PACKET_STATE_UPDATE_LOCATION, PACKET_STATE_DELIVERED
import json
import threading

from packet_model import PacketStore

'''
This consumer listens to the topic packet and builds the internal packet history
model.
'''
class TrackingService:

        '''
        consumer: A consumer listening to the topic packet
        '''
        def __init__(self, consumer, updateCallback = None, deliverCallback = None):
            self.consumer = consumer
            self.consumerThread = 0
            self.packetStore = PacketStore(updateCallback, deliverCallback)
            self.readPackets()

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

            if eventVersion != 3:
                #print('Unexpected event version (expected: 1, found: ' + str(eventVersion) + ')')
                return

            if eventType == PACKET_STATE_REGISTERED:
                self.packetStore.addPacket(eventTime, eventPayload)

            if eventType == PACKET_STATE_UPDATE_LOCATION:
                self.packetStore.updatePacket(eventTime, eventPayload)

            if eventType == PACKET_STATE_DELIVERED:
                self.packetStore.packetDelivered(eventTime, eventPayload)

        '''
        start consuming the whole kafka log to create packet model
        '''
        def readPackets(self):
            print('Starting packet reading...')

            if(self.consumerThread == 0):
                self.consumerThread = threading.Thread(target=self.startConsuming)
                self.consumerThread.start()
                return "Consumer started and reading packets."
            else:
                return "Consumer already running."

        '''
        Returns the packet status of the given packet_id or None no packet was found
        '''
        def packetStatus(self, packet_id):
            dictPacketStatus = self.packetStore.packetStatus(packet_id)
            return dictPacketStatus
