import json
from kafka import KafkaProducer, KafkaConsumer
import time


'''
Creates and returns a producer that is connected to a kafka service via url and port.
serializer is optional and is used to transform the data sent with the returned producer.
By default, serializer will encode the data to json
'''
def create_producer(url, port, serializer = lambda m: json.dumps(m).encode('utf-8')):
    return KafkaProducer(bootstrap_servers=url+":"+str(port),
                         value_serializer=serializer)
'''
Creates and returns a consumer that is connected to a kafka service via url and port.
The consumer receives data from the given topic.
If from_beginning is specified, the consumer will receive all events in the topic,
if not it will only receive events that enter the event store after the consumer 
has been created
'''
def create_consumer(url, port, topic, from_beginning = True):
    return KafkaConsumer(topic,bootstrap_servers=url+":"+str(port),
                         auto_offset_reset='earliest' if from_beginning else 'latest')
    
'''
Sends an asynchronous event to the given topic using the given producer.
event_type: string that describes the type of the event to send
version: int
payload (optional): dictionary that contains payload data for this event
'''
def send(producer, topic, event_type, version, payload = None):
    message = {}
    message['version'] = version
    message['type'] = event_type
    message['time'] = int(time.time())
    if payload:
        message['payload'] = payload
    return producer.send(topic, message)

'''
Sends an event to the given topic using the given producer. A KafkaError is raised
in case if this event was not received by kafka.
In other words: Waits (blocking!) for an acknowledgement from the kafka service
'''
def sendSync(producer, topic, event_type, version, payload = None):
    meta = send(producer, topic, event_type, version, payload)
    return meta.get(timeout=10)#This raises KafkaError on failure

'''
Blockingly reads events from the given consumer. These events are delivered to
trackingService.consumeEvent(data) where data is the data of this event as string
''' 
def readFromStart(consumer, trackingService):
    for message in consumer:
        trackingService.consumeEvent(message.value.decode('utf-8'))
        