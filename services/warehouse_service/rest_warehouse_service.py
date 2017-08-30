#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import random
from flask import Flask, request

sys.path.append(os.path.relpath('../common'))
sys.path.append(os.path.relpath('../rest_common'))
sys.path.append(os.path.relpath('../mykafka'))
import rest_common
from warehouse_service import WarehouseService
import mykafka



app = Flask(__name__)#Initialize flask

srv = WarehouseService(mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'packet'))

'''
This function is called whenever a client visits the '/packetStatus' "page" on
this server.
'''
@app.route('/getRegistrationsPerDay', methods=['GET'])
def restPacketStatus():
    #res = {"values": srv.getListbyRegistrationDay('%Y-%m-%d')}
    byhour = srv.getCountOfRegistrationByTime('%H')
    hours = range(24)
    res = {"values": { hour : 0 for hour in hours}}
    
    for hour, count in byhour.items():
        res["values"][int(hour)] = count
    print(res)
    
    return rest_common.create_response(200, res)

@app.route('/getAverageDeliveryTime', methods=['GET'])
def restPacketStatus():
    # res = {"values": srv.getListbyRegistrationDay('%Y-%m-%d')}
    byhour = srv.getAverageDeliveryTime('%H')
    hours = range(24)
    res = {"values": {hour: 0 for hour in hours}}

    for hour, count in byhour.items():
        res["values"][int(hour)] = count
    print(res)

    return rest_common.create_response(200, res)

@app.route('/getSizeDistribution', methods=['GET'])
def getSizeDistribution():
    res = {"values" : srv.getCountOfKey("size") }

    return rest_common.create_response(200, res)


if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(debug=True, host='0.0.0.0', port=port)