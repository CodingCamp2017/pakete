from post_service import PostService
import sys
import os
sys.path.append(os.path.relpath('../mykafka'))
import mykafka
from random import sample, random, randint
import json
import codecs

sizes = ['small','normal','big']

fakedata = json.load(codecs.open('fakedata.json', 'r', 'utf-8-sig'))['data']

def create_random_package():
    sender = fakedata[randint(0, len(fakedata))]
    receiver = fakedata[randint(0, len(fakedata))]
    package = {}
    package['sender_name'] = sender['name']
    package['sender_street'] = sender['street']
    package['sender_ZIP'] = randint(10000,99999)
    package['sender_city'] = sender['city']
    package['receiver_name'] = receiver['name']
    package['receiver_street'] = receiver['street']
    package['receiver_ZIP'] = randint(10000,99999)
    package['receiver_city'] = receiver['city']
    package['size'] = sizes[randint(0,3)]
    package['weight'] = sender['weight']
    package = json.dumps(package)
    return package


post_service = PostService(mykafka.create_producer('ec2-35-159-21-220.eu-central-1.compute.amazonaws.com', 9092))

registered_packages = []
