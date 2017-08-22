# -*- coding: utf-8 -*-
from Exceptions import InvalidActionException, CommandFailedException

import sys
import os
sys.path.append(os.path.relpath('../mykafka'))

import mykafka
import re
import json

class Package:
    pass

class TrackingService:
        def __init__(self, consumer):
            self.consumer = consumer
        
        # read the whole kafka log and create package model
        def read_packages(self):
            print('read_packages')
            mykafka.read_from_start(self.consumer)
            return "blub"

        def package_status(self, jsons):
            #jobj = ? # convert json string to object
            package_id = 0 # jobj['id']
            return "status of package" + package_id