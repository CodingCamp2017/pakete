#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading

class ClientSubscriptionManager:
    def __init__(self):
        self.subscribed_ids = {}#dict packet_id -> list of client session ids
        self.subscribed_clients = {}#dict client session id -> list of packet_ids
        self.id_lock = threading.Lock()
        self.client_lock = threading.Lock()
        
    def client_connected(self, sid):
        with self.client_lock:
            if not sid in self.subscribed_clients:
                self.subscribed_clients[sid] = list()
            print("Client ("+sid+") connected")
    
    def client_subscribe(self, sid, packet_id):
        subs = 0
        clients = 0
        with self.client_lock:
            self.subscribed_clients[sid].append(packet_id)
            subs = len(self.subscribed_clients[sid])
        with self.id_lock:
            client_list = self.subscribed_ids.get(packet_id, list())
            client_list.append(sid)
            self.subscribed_ids[packet_id] = client_list
            clients = len(client_list)
        p{'2017-08-28 16': {'summWeight': 12.566106152, 'count': 4, 'averageWeight': 3.141526538}, '2017-08-28 17': {'summWeight': 3.141526538, 'count': 1, 'averageWeight': 3.141526538}, '2017-08-29 09': {'summWeight': 1234.0, 'count': 1, 'averageWeight': 1234.0}, '2017-08-29 10': {'summWeight': 9.0, 'count': 3, 'averageWeight': 3.0}, '2017-08-29 11': {'summWeight': 16420.0, 'count': 100, 'averageWeight': 164.2}, '2017-08-29 12': {'summWeight': 3200.0, 'count': 16, 'averageWeight': 200.0}, '2017-08-29 13': {'summWeight': 3067.0, 'count': 57, 'averageWeight': 53.80701754385965}, '2017-08-29 14': {'summWeight': 288492.3, 'count': 3616, 'averageWeight': 79.78216261061947}, '2017-08-29 15': {'summWeight': 19200.0, 'count': 96, 'averageWeight': 200.0}, '2017-08-29 16': {'summWeight': 172906.8, 'count': 3213, 'averageWeight': 53.81475256769374}}
rint("Client ("+sid+") subscribed to "+packet_id+", total_subs="+str(subs)+", packet is subscribed by "+str(clients))
            
    def client_disconnect(self, sid):
        ids = list()
        revoked_subs = 0
        with self.client_lock:
            ids = list(self.subscribed_clients[sid])
            del self.subscribed_clients[sid]
        with self.id_lock:
            for packet_id in ids:
                clients = self.subscribed_ids[packet_id]
                clients.remove(sid)
                self.subscribed_ids[packet_id] = clients
                if len(clients) == 0:
                    del self.subscribed_ids[packet_id]
                    revoked_subs = revoked_subs+1
        print("Client ("+sid+") disconnected; subscribed_ids="+str(len(ids))+", revoked="+str(revoked_subs))
                    
    def get_subscribed_clients_for_id(self, packet_id):
        clients = None
        with self.id_lock:
            if packet_id in self.subscribed_ids:
                clients = list(self.subscribed_ids[packet_id])#copy list
        return clients#return copy
                