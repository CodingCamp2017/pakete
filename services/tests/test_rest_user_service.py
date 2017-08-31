import json
import urllib
import urllib.request
import uuid
import time

url = 'http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com'
port = ':8002'
headers = {"Content-Type":"application/json"}

user = {'email' : 'vsadjfb@vxcvasnc.com', 'password' : 'sdf34534'}

# test restAddUser()
request = urllib.request.Request(url+port+'/add_user', data=json.dumps(user).encode('utf8'), headers=headers)
try:
    urllib.request.urlopen(request)
    print('Successfully added user')
except urllib.error.HTTPError as e:
    if e.code == 409:
        print('User exists')
    else:
        print(e)

# test restAuthenticateUser()
request = urllib.request.Request(url+port+'/authenticate_user', data=json.dumps(user).encode('utf8'), headers=headers)
try:
    response = urllib.request.urlopen(request)
    session_id = json.loads(response.read().decode("utf-8"))['session_id']
    print('Successfully authenticated user')
except urllib.error.HTTPError as e:
    print(e)


# test restAddPacket()
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
request = urllib.request.Request(url+':8000' + '/register', data=json.dumps(packet).encode('utf8'), headers = headers)
try:
    response = urllib.request.urlopen(request)
    packet_id = json.loads(response.read().decode("utf-8"))['packet_id']
    print('Successfully registered packet: '+packet_id)
except:
    print('Register went wrong')
time.sleep(1) # wait for id_store to update
data = {'session_id' : session_id, 'packet_id' : packet_id}
request = urllib.request.Request(url+port+'/add_packet_to_user', data=json.dumps(data).encode('utf8'), headers=headers)
try:
    urllib.request.urlopen(request)
    print('Successfully added packet to user')
except urllib.error.HTTPError as e:
    print(e, e.msg)


# test restGetPacket(session_id)
request = urllib.request.Request(url+port+'/get_packets_from_user/'+session_id, headers=headers)
try:
    response = urllib.request.urlopen(request)
    packets = json.loads(response.read().decode("utf-8"))['packets']
    print('Successfully got packets from user: '+str(packets))
except urllib.error.HTTPError as e:
    print(e)



# test restLogoutUser()
data = {'session_id' : session_id}
request = urllib.request.Request(url+port+'/logout', data=json.dumps(data).encode('utf8'), headers=headers)
try:
    urllib.request.urlopen(request)
    print('Successfully logged out')
except urllib.error.HTTPError as e:
    print(e, e.msg)


# test restDeleteUser()
request = urllib.request.Request(url+port+'/authenticate_user', data=json.dumps(user).encode('utf8'), headers=headers)
try:
    response = urllib.request.urlopen(request)
    session_id = json.loads(response.read().decode("utf-8"))['session_id']
    print('Successfully authenticated user')
except urllib.error.HTTPError as e:
    print(e, e.msg, e.info, e.strerror)
data = {'session_id' : session_id}
request = urllib.request.Request(url+port+'/delete_user', data=json.dumps(data).encode('utf8'), headers=headers)
try:
    urllib.request.urlopen(request)
    print('Successfully deleted user')
except urllib.error.HTTPError as e:
    print(e, e.msg, e.info, e.strerror)
