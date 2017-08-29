from FakeDataProvider import FakeDataProvider
from random import randint
import urllib.request

import threading
import time
import json
import multiprocessing

class RestSimulation():
    def __init__(self, baseurl, headers, fakeDataProvider):
        self.baseurl = baseurl
        self.headers = headers
        self.fakeDataProvider = fakeDataProvider
        self.threadStop = threading.Event()
        self.packetList = list()
        self.lock = threading.Lock()

    def registerRandomPackets(self):
        print("Started registering")
        while not self.threadStop.is_set():
            #print("register")
            packet = self.fakeDataProvider.getRandomPacket()
            registerRequest = urllib.request.Request(self.baseurl + 'register',
                data = json.dumps(packet).encode('utf8'),
                headers = self.headers)
            response = urllib.request.urlopen(registerRequest)
            responseJson = json.loads(response.read().decode('utf8'))
            self.packetList.append(responseJson['id'])
            #time.sleep(randint(100,200)/1000.0)
        print("register stoped")

    def updateRandomPackets(self):
        print("Started updating")
        while not self.threadStop.is_set():
            if len(self.packetList) < 1:
                continue
            data = {}
            data['station'] = self.fakeDataProvider.getRandomCity()
            data['vehicle'] = self.fakeDataProvider.getRandomVehicle()
            with self.lock:
                #print("update")
                id = self._getRandomId()
                updateRequest = urllib.request.Request(self.baseurl + 'packet/' + id +'/update',
                                                       data = json.dumps(data).encode('utf8'),
                                                       headers = self.headers)
                urllib.request.urlopen(updateRequest)
            #time.sleep(randint(100,200)/1000.0)
        print("update stoped")

    def deliverRandomPackets(self):
        print("Started delivering")
        while not self.threadStop.is_set():
            if len(self.packetList) < 1:
                continue
            with self.lock:
                #print("deliver")
                id = self._getRandomId()
                deliverRequest = urllib.request.Request(self.baseurl + 'packet/' + id +'/delivered',
                                                        data=json.dumps({}).encode('utf8'),
                                                        headers = self.headers)
                urllib.request.urlopen(deliverRequest)
                self.packetList.remove(id)
            #time.sleep(randint(100,200)/1000.0)
        print("deliver stoped")
    
    def _getRandomId(self):
        while len(self.packetList) < 1:
            time.sleep(0.1)
        return self.packetList[randint(0,len(self.packetList)-1)]
    
    def stopThreads(self):
        self.threadStop.set()

if __name__ == '__main__':
    SIMULATION_TIME = 120 # Seconds
    fakeDataProvider = FakeDataProvider('fakedata.json')
    restSimulation = RestSimulation('http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8000/',
                                    {"Content-Type":"application/json"},
                                    fakeDataProvider)
    restSimulation.threadStop.clear()
    threads = list()
    for i in range(int(multiprocessing.cpu_count()/2)):
        threads.append(threading.Thread(target=restSimulation.registerRandomPackets))
        threads.append(threading.Thread(target=restSimulation.updateRandomPackets))
    threads.append(threading.Thread(target=restSimulation.deliverRandomPackets))
    
    for t in threads:
        t.daemon = True
        t.start()

    time.sleep(SIMULATION_TIME)