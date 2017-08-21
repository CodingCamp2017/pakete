# include kafka-python library
import sys
sys.path.insert(0, '/home/j/CodingCamp/kafka_python/')
import json
from kafka import KafkaProducer, KafkaConsumer
from post_service.post_service import register_package

value_serializer=lambda m: json.dumps(m).encode('ascii')

producer = KafkaProducer(bootstrap_servers='ec2-35-159-21-220.eu-central-1.compute.amazonaws.com:9092',
                         value_serializer=lambda m: json.dumps(m).encode('ascii'))

consumer = KafkaConsumer('test-json2',
                         bootstrap_servers='ec2-35-159-21-220.eu-central-1.compute.amazonaws.com:9092',
                         value_deserializer=lambda m: json.loads(m.decode('ascii')),
                         auto_offset_reset='earliest')

dummy_package = {'bla' : 'blup'}
package_id = register_package(dummy_package, producer)
producer.flush()
print('flushed')

producer.close()
print('closed')

#consumer.topics()
#consumer.seek_to_beginning()

for message in consumer:
    print (message)
