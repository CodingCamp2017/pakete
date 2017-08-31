import distribution_service
import threading
import signal

post_service_url_local = 'http://0.0.0.0:8000'
post_service_url_server = 'http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8000'

threadStop = threading.Event()

def sigint_handler(signum, frame):
    print('Interrupted')
    threadStop.set()

signal.signal(signal.SIGINT, sigint_handler)

threadStop.clear()

idstore = distribution_service.idstore

threads = list()
for i in range(distribution_service.MAX_NUMBER):
    threads.append(distribution_service.DistributionService(i, idstore, post_service_url_server, threadStop))

for t in threads:
    t.daemon = True
    t.start()