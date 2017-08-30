from Exceptions import InvalidActionException
import Exceptions
import re
import json

regex_name = '[\w ]+'#Multiple words separated by spaces
regex_id = '(\d|[a-f]){8}-(\d|[a-f]){4}-(\d|[a-f]){4}-(\d|[a-f]){4}-(\d|[a-f]){12}'#uuid format: 8-4-4-4-12 chars in hex range
regex_zip = '\d{5}'#zipcode is exaclty 5 digits
regex_street = '[\w( \-\.)?]+'#multiple word separated either by spaces, '.' or '-'
regex_city = '[\w( \/\.\-)?]+'#multiple word separated either by spaces, '-'
regex_size = '(small|normal|big)'
regex_weight = '[+-]?(\d*\.)?\d+'#a floating point value, decimal separator is '.'
regex_vehicle = '(car|foot|plane|rocket|ship|train|truck|center|failed)'
regex_email = '[\w\d.+]+@[\w\d]+(?:\.[a-z]{2,4}){1,2}'
regex_password = '\w{8}'#8 char password
regex_session_id = '[\w-]+'#alphanumeric and '-'
'''
This lists the required keys and a regex for the value of the registerPacket
command
'''
syntax_register = [('sender_name', regex_name),
                   ('sender_street',regex_street), 
                   ('sender_zip', regex_zip), 
                   ('sender_city', regex_city),
                   ('receiver_name', regex_name),
                   ('receiver_street', regex_street), 
                   ('receiver_zip', regex_zip),
                   ('receiver_city', regex_city), 
                   ('size', regex_size), 
                   ('weight', regex_weight)]
'''
This lists the required keys and a regex for the value of the updateLocation
command
'''
syntax_update = [('packet_id', regex_id),
                 ('station', regex_city),
                 ('city', regex_city),
                 ('zip', regex_zip),
                 ('street', regex_street),
                 ('vehicle', regex_vehicle)]
'''
This lists the required keys and a regex for the value of the delivered command
'''
syntax_delivered = [('packet_id', regex_id)]
'''
This lists the required keys and a regex for the value of the addUser command
'''
syntax_add_user = [('email', regex_email),
                   ('password', regex_password)]
'''
This lists the required keys and a regex for the value of the authenticateUser
command
'''
syntax_authenticate_user = [('email', regex_email),
                            ('password', regex_password)]
'''
This lists the required keys and a regex for the value of the updateAddress command
'''
syntax_update_user_adress = [('email', regex_email),
                             ('street', regex_street),
                             ('zip', regex_zip), 
                             ('city', regex_city),
                             ('session_id', regex_session_id)]
'''
This lists the required keys and a regex for the value of the addPacketToUser command
'''
syntax_add_packet_to_user = [('packet_id', regex_id),
                             ('session_id', regex_session_id)]
'''
This lists the required keys and a regex for the value of commands that require only a session id
'''
syntax_session_id = [('session_id', regex_session_id)]

'''
Returns True only if the given string fully matches the given regex.
This will return False if any substring matches or if the string does not match
'''
def regex_matches_exactly(regex, string):
        compRegex = re.compile(regex)
        match = compRegex.match(string)
        return match != None and match.end() == len(string)

'''
Returns the first key from the given dictionary that is not present in req_list.
Returns None if every key in the dictionary is present in req_list.
'''
def get_first_not_contained(dic, req_list):
    req_list_keys = [key for (key, value) in req_list]
    for (key, value) in dic:
        if(not key in req_list_keys):
            return key
    return None

'''
Checks if the given dictionary contains exactly the keys of req_list and matches
the value of each key with the respective regex.
Raises Exception.InvalidActionException if the check is false
'''
def check_json_regex(dic, req_list):
    for (key, regex) in req_list:
        if(not key in dic):
            raise InvalidActionException(Exceptions.TYPE_KEY_NOT_FOUND, key, "Required key: "+key)
        elif(not isinstance(dic[key],str)):
            raise InvalidActionException(Exceptions.TYPE_INVALID_KEY, key, "Invalid type for key "+key+"; expected string")
        elif(not regex_matches_exactly(regex, dic[key])):
            raise InvalidActionException(Exceptions.TYPE_INVALID_KEY, key, "Invalid value: "+str(dic[key])+" for key "+key)
    if(len(dic) != len(req_list)):
        raise InvalidActionException(Exceptions.TYPE_INVALID_KEY, str(get_first_not_contained(dic, req_list)), "Unknown keys in "+json.dumps(dic))
                
def test_check_json_regex():
    req = [("a", "\\d{2}"), ("b", "hgf")]
    dic = {'a':'45', 'b':'hgf'}
    check_json_regex(dic, req)
    print("test_checkAvailable#1")
    dic['a'] = 'a1'
    try:
        check_json_regex(dic, req)
        raise AssertionError('test_checkAvailable')
    except InvalidActionException:
        pass
    print("test_checkAvailable#2")
        
    dic2 = {'a':'12', 'b':'fgtd', 'c':'wer'}
    try:
        check_json_regex(dic2, req)
        raise AssertionError('test_checkAvailable2')
    except InvalidActionException as e:
        pass
    print("test_checkAvailable#3")
    dic3 = {'a':'16'}
    try:
        check_json_regex(dic3, req)
        raise AssertionError('test_checkAvailable3')
    except InvalidActionException as e:
        pass
    print("test_checkAvailable#4")
          

        
    
        
if __name__ == '__main__':
    test_check_json_regex()
