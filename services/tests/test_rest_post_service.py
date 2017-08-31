import json
import urllib

local_post_host = 'http://0.0.0.0:34239/'
local_tracking_host = 'http://0.0.0.0:34239/'
app_host = 'http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8000'

packet = {'sender_name' : 'Otto Hahn',
          'sender_street' : 'Veilchenweg 2324',
          'sender_zip' : '12345',
          'sender_city' : 'Hamburg',
          'receiver_name' : 'Lise Meitner',
          'receiver_street' : 'Amselstraße 7',
          'receiver_zip' : '01234',
          'receiver_city' : 'Berlin',
          'size' : 'big',
          'weight' : '200'}

registerRequest = urllib.request.Request(app_host + '/register',
                                        data=json.dumps(packet).encode('utf8'),
                                        headers = {"Content-Type":"application/json"})
try:
    urllib.request.urlopen(registerRequest)
except:
    print('Register went wrong')

response = urllib.request.urlopen(registerRequest)
responseJson = json.loads(response.read().decode('utf8'))

packet_id = responseJson['packet_id']

updateData = {'station' : 'Berlin', 'vehicle' : 'car'}

updateRequest = urllib.request.Request(app_host + '/packet/'+packet_id+'/update',
                                       data=json.dumps(updateData).encode('utf8'),
                                       headers = {"Content-Type":"application/json"})

urllib.request.urlopen(updateRequest)


deliverRequest = urllib.request.Request(app_host + '/packet/' + packet_id +'/delivered',
                                        data=json.dumps({}).encode('utf8'),
                                        headers = {"Content-Type":"application/json"})
try:
    urllib.request.urlopen(deliverRequest)
except urllib.error.HTTPError as e:
    error_message = e.read()
    print(error_message)