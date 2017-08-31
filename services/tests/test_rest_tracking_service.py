import json
import urllib.request

url = 'http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com'
post_port = 8000
tracking_port = 8001
headers = {"Content-Type":"application/json"}

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

def registerPacket():
    registerRequest = urllib.request.Request(url + ':' + str(post_port) + '/register',
                                        data=json.dumps(packet).encode('utf8'),
                                        headers = {"Content-Type":"application/json"})
    try:
        response = urllib.request.urlopen(registerRequest)
        responseJson = json.loads(response.read().decode('utf8'))
        print('Register completed.')
        return responseJson
    except:
        print('Register went wrong')
        exit(0)

def trackPacket(packet_id):
    trackingRequest = urllib.request.Request(url + ':' + str(tracking_port) + '/packetStatus/' + packet_id,
                                        headers = {"Content-Type":"application/json"})
    try:
        response = urllib.request.urlopen(trackingRequest)
        responseJson = json.loads(response.read().decode('utf8'))
        print('Tracking completed.')
        return responseJson
    except Exception as e:
        print('Tracking went wrong')
        exit(0)

if __name__ == '__main__':
    packet_id = registerPacket()['packet_id']
    trackPacket(packet_id)
