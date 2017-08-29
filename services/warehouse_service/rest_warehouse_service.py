#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from flask import Flask, request

sys.path.append(os.path.relpath('../common'))
sys.path.append(os.path.relpath('../rest_common'))
sys.path.append(os.path.relpath('../mykafka'))
import rest_common


app = Flask(__name__)#Initialize flask

'''
This function is called whenever a client visits the '/packetStatus' "page" on
this server.
'''
@app.route('/get', methods=['GET'])
def restPacketStatus():
    res = {"values" : [1,2,3,4]}
    return rest_common.create_response(200, res)

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(debug=True, host='0.0.0.0', port=port)