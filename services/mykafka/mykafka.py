
#'ec2-35-159-21-220.eu-central-1.compute.amazonaws.com:9092'

import json
from kafka import KafkaProducer, KafkaConsumer
import time

def create_producer(url, port, serializer = lambda m: json.dumps(m).encode('utf-8')):
    return KafkaProducer(bootstrap_servers=url+":"+str(port),
                         value_serializer=serializer)
    
def create_consumer(url, port, topic, deserializer = lambda m: json.loads(m.decode('utf-8')), from_beginning = True):
    return KafkaConsumer(topic,bootstrap_servers=url+":"+str(port),
                         #value_deserializer=deserializer, # crashes if input not in json format
                         auto_offset_reset='earliest' if from_beginning else 'latest')
    
    
def send(producer, topic, event_type, version, payload = None):
    message = {}
    message['version'] = version
    message['type'] = event_type
    message['time'] = int(time.time())
    if payload:
        message['payload'] = payload
    return producer.send(topic, message)
    
def sendSync(producer, topic, event_type, version, payload = None):
    meta = send(producer, topic, event_type, version, payload)
    return meta.get(timeout=10)#This raises KafkaError on failure
    
def readFromStart(consumer, trackingService):
    for message in consumer:
        trackingService.consumeEvent(message.value.decode('utf-8'))
        