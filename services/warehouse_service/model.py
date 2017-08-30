import threading
import datetime
class Model:


    def __init__(self, initData = {}):
        self.packets = initData
        self.packets.items().__iter__()
        self.lock = threading.Lock()
    #End Constructor

    def set(self,key,value):
        with self.lock:
            self.packets[key] = value
        return
    #End Method

    def get(self,key):
        with self.lock:
            return self.packets[key]
    #End Method

    def append(self,key,value):
        with self.lock:
            self.packets[key].append(value)
        return
    # End Method

    def size(self):
        return len(self.packets)
    #End Method

    def getDate(self, timefilter):
        with self.lock:
            return datetime.datetime.fromtimestamp(int(self.packets['register_time'])).strftime(timefilter)
    #End Method

    def has(self,key):
        with self.lock:
            return key in self.packets
    #End Method

    #Threadsafe ReadOnly
    def for_each(self, consumer):
        with self.lock:
            for key, value in self.packets:
                consumer(key, value)
    #End Method

    #Threadsafe ReadAndAddOnly
    def items(self,filter = None):
        if filter == None:
            with self.lock:
                return {key: value for (key, value) in self.packets.items()}.items()
        return self.__items(filter);
    #End Method

            # Threadsafe ReadAndAddOnly

    def __items(self,filter):
        with self.lock:
            tempPack = {}
            for (key, value) in self.packets.items():
                if not filter.accept(int(value.get('register_time'))):
                    continue
                tempPack[key] = value
            return tempPack.items()
            # End Method

    def copy_dict(d):
        return {key: value for (key, value) in d.items()}
    #End Method

    '''def __str__(self):
        return self.packets.__str__()
    def __repr__(self):
        return self.__str__()'''
