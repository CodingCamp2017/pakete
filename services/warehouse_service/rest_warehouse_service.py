#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import random
from flask import Flask, request

sys.path.append(os.path.relpath('../common'))
import packet_regex
sys.path.append(os.path.relpath('../rest_common'))
sys.path.append(os.path.relpath('../mykafka'))
import rest_common
from warehouse_service import WarehouseService, Filter
import mykafka

app = Flask(__name__)#Initialize flask

srv = WarehouseService(mykafka.create_consumer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092, 'packet'))

groupby_map = {
    'hour':'%H',
    'day':'%Y%m%d',
    'week':'%A'
}


def _tagname(tag):
    return {tag:lambda f:srv.getCountOfKey(tag, filter = f)}

info_map = {
    'location_vehicle_current':lambda f:srv.getCountOfCurrendLocationOfPackets(filter=f),
    'location_address_current':lambda f:srv.getCountOfCurrendLocationOfPackets(True, filter=f)
}
info_map.update(_tagname('sender_street'))
info_map.update(_tagname('sender_zip'))
info_map.update(_tagname('sender_city'))
info_map.update(_tagname('receiver_street'))
info_map.update(_tagname('receiver_zip'))
info_map.update(_tagname('receiver_city'))
info_map.update(_tagname('size'))

info_group_map = {
    'average_delivery':srv.getAverageDeliveryTimeByTime,
    'average_weight':srv.getAverageWeightByTime,
    'registration':srv.getCountOfRegistrationByTime,
    'location_vehicle_current':lambda group, f:srv.getCountOfLacationByTime(group, ByName=False, onlyCurrentLocation=True, onlyUndeliveryed=False, filter = f),
    'location_vehicle_alltime':lambda group, f:srv.getCountOfLacationByTime(group, ByName=False, onlyCurrentLocation=False, onlyUndeliveryed=False, filter = f),
    'location_address_current':lambda group, f:srv.getCountOfLacationByTime(group, ByName=True, onlyCurrentLocation=True, onlyUndeliveryed=False, filter = f),
    'location_address_alltime':lambda group, f:srv.getCountOfLacationByTime(group, ByName=True, onlyCurrentLocation=False, onlyUndeliveryed=False, filter = f)
}
def _tagname_group(tag):
    return {tag:lambda group, f:srv.getCountOfKeyByTime(tag, group, filter = f)}

info_group_map.update(_tagname_group('sender_street'))
info_group_map.update(_tagname_group('sender_zip'))
info_group_map.update(_tagname_group('sender_city'))
info_group_map.update(_tagname_group('receiver_street'))
info_group_map.update(_tagname_group('receiver_zip'))
info_group_map.update(_tagname_group('receiver_city'))
info_group_map.update(_tagname_group('size'))

def _check_input(fromtime, to, information, map):
    if not packet_regex.regex_matches_exactly(packet_regex.regex_timestamp, fromtime):
        return rest_common.create_error_response(400, 'Unknown from timestamp')
    if not packet_regex.regex_matches_exactly(packet_regex.regex_timestamp, to):
        return rest_common.create_error_response(400, 'Unknown to timestamp')
    if not information in map:
        return rest_common.create_error_response(400, 'Unkown information request')
    return None

@app.route('/<fromtime>/<to>/<information>/<groupby>', methods=['GET'])
def restQueryWithGroup(fromtime, to, information, groupby):
    error = _check_input(fromtime, to, information, info_group_map)
    if error:
        return error
    if not groupby in groupby_map:
        return rest_common.create_error_response(400, 'Unknown groupby value')
    #call function
    f = Filter(int(fromtime), int(to))
    result = info_group_map[information](groupby_map[groupby], f)
    return rest_common.create_response(200, {'values':result})

@app.route('/<fromtime>/<to>/<information>', methods=['GET'])
def restQueryWithoutGroup(fromtime, to, information):
    error = _check_input(fromtime, to, information, info_map)
    if error:
        return error
    #call function
    f = Filter(int(fromtime), int(to))
    result = info_map[information](f)
    return rest_common.create_response(200, {'values':result})

@app.route('/<information>/<groupby>', methods=['GET'])
def restDefaultQueryWithGroup(information, groupby):
    return restQueryWithGroup('0', '-1', information, groupby)

@app.route('/<information>', methods=['GET'])
def restDefaultQueryWithoutGroup(information):
    return restQueryWithoutGroup('0', '-1', information)

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(debug=True, host='0.0.0.0', port=port)
