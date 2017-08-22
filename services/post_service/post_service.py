from datetime import datetime

def produce_event(package_id, event_type, producer, package=None):
    message = {}
    message['id'] = package_id
    message['type'] = event_type
    message['time'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    if package:
        message['payload'] = package
    #producer.send('packages', b'hello!')
    producer.send('packages', message)

def assign_package_id():
    return 0

def register_package(package, producer):
    package_id = assign_package_id()
    produce_event(package_id, 'registered', producer, package)
    return package_id

def update_package_location(package_id, location, producer):
    produce_event(package_id, 'updated', producer)
    
def mark_delivered(package_id, producer):
    produce_event(package_id, 'delivered', producer)