from random import randint
import http.client
import codecs
import threading
import time
import json
import signal
import multiprocessing

class Provider():
    def __init__(self, file, rootName):
        self.data = json.load(codecs.open(file, 'r', 'utf-8-sig'))[rootName]
        print("File "+file+" contains "+str(len(self.data))+" elements")
        
    def getRandom(self):
        return self.data[randint(0,len(self.data)-1)]

class TransportSimulation():
    def __init__(self, baseurl, headers, nameProvider, addressProvider):
        self.baseurl = baseurl
        self.headers = headers
        self.nameProvider = nameProvider
        self.addressProvider = addressProvider
        self.threadStop = threading.Event()
        self.sizes = ['small', 'normal', 'big']
        
    def getRandomSize(self):
        return self.sizes[randint(0, len(self.sizes)-1)]

    def registerRandomPackets(self):
        print("Started registering")
        connection = http.client.HTTPConnection(self.baseurl)
        while not self.threadStop.is_set():
            #print("register")
            name1 = self.nameProvider.getRandom()
            address1 = self.addressProvider.getRandom()
            name2 = self.nameProvider.getRandom()
            address2 = self.addressProvider.getRandom()
            packet = {'sender_name':name1,
                      'sender_street':address1['street'],
                      'sender_zip':str(address1['zip']),
                      'sender_city':address1['city'],
                      'receiver_name':name2,
                      'receiver_street':address2['street'],
                      'receiver_zip':str(address2['zip']),
                      'receiver_city':address2['city'],
                      'size':self.getRandomSize(),
                      'weight':str(randint(0, 100))}
            #print(str(packet))
            connection.request("POST", '/register', body=json.dumps(packet).encode('utf8'), headers = self.headers)
            response = connection.getresponse()
            if response.code != 200:
                print(str(response.code)+": "+str(response.read()))
            #time.sleep(randint(100,200)/1000.0)
        connection.close()
        print("register stoped")
    
    def stopThreads(self):
        self.threadStop.set()

if __name__ == '__main__':
    SIMULATION_TIME = 120 # Seconds
    nameProvider = Provider('names.json', 'names')
    addrProvider = Provider('addresses.json', 'addresses')
    transportSimulation = TransportSimulation('ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8000',
                                    {"Content-Type":"application/json"},
                                    nameProvider, addrProvider)
    transportSimulation.threadStop.clear()
    threads = list()
    for i in range(int(multiprocessing.cpu_count()/2)):
        threads.append(threading.Thread(target=transportSimulation.registerRandomPackets))
    
    for t in threads:
        t.daemon = True
        t.start()
        
    def sigint_handler(signum, frame):
        print('Interrupted')
        transportSimulation.threadStop.set()
    
    signal.signal(signal.SIGINT, sigint_handler)

    time.sleep(SIMULATION_TIME)
    transportSimulation.threadStop.set()