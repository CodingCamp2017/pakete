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
        print("Client ("+sid+") subscribed to "+packet_id+", total_subs="+str(subs)+", packet is subscribed by "+str(clients))
            
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
                