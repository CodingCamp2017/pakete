import json
import urllib
import uuid

url = 'http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com'
port = ':8002'
headers = {"Content-Type":"application/json"}

user = {'email' : 'blaaa@codingcamp.de', 'password' : '12345678'}

# test restAddUser()
request = urllib.request.Request(url+port+'/add_user', data=json.dumps(user).encode('utf8'), headers=headers)
urllib.request.urlopen(request)
try:
    urllib.request.urlopen(request)
    print('Successful added user')
except urllib.error.HTTPError as e:
    print(e, e.msg)

# test restAuthenticateUser()
request = urllib.request.Request(url+port+'/authenticate_user', data=json.dumps(user).encode('utf8'), headers=headers)
response = urllib.request.urlopen(request)
session_id = json.loads(response.read().decode("utf-8"))['session_id']
print('Successful authenticated user')


# test restAddPacket()
data = {'session_id' : session_id, 'packet' : str(uuid.uuid1())}
request = urllib.request.Request(url+port+'/add_packet_to_user', data=json.dumps(data).encode('utf8'), headers=headers)
try:
    urllib.request.urlopen(request)
    print('Successful added packet to user')
except urllib.error.HTTPError as e:
    print(e, e.msg)


# test restGetPacket(session_id)
data = {'session_id' : session_id}
request = urllib.request.Request(url+port+'/get_packets_from_user/'+session_id, data=json.dumps(data).encode('utf8'), headers=headers)
response = urllib.request.urlopen(request)
packets = json.loads(response.read().decode("utf-8"))['session_id']
print('Successful got packet from user')


# test restLogoutUser()
data = {'session_id' : session_id}
request = urllib.request.Request(url+port+'/logout', data=json.dumps(data).encode('utf8'), headers=headers)
urllib.request.urlopen(request)
print('Successful logged out')


# test restDeleteUser()
request = urllib.request.Request(url+port+'/authenticate_user', data=json.dumps(user).encode('utf8'), headers=headers)
response = urllib.request.urlopen(request)
session_id = json.loads(response.read().decode("utf-8"))['session_id']
data = {'session_id' : session_id}
request = urllib.request.Request(url+port+'/delete_user', data=json.dumps(data).encode('utf8'), headers=headers)
urllib.request.urlopen(request)
print('Successful deleted user')