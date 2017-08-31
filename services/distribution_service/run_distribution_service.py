import distribution_service
import threading
import signal

post_service_url = 'http://0.0.0.0:8000'
BASEURL = 'ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8000'

threadStop = threading.Event()

def sigint_handler(signum, frame):
    print('Interrupted')
    threadStop.set()

signal.signal(signal.SIGINT, sigint_handler)

threadStop.clear()

threads = list()
for i in range(distribution_service.MAX_NUMBER):
    threads.append(distribution_service.DistributionService(i, threadStop, post_service_url))

for t in threads:
    t.daemon = True
    t.start()