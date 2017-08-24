from Exceptions import InvalidActionException
import Exceptions
import re
import json

regex_name = '[\w ]+'
regex_id = '[\w-]+'
regex_zip = '\d{5}'
regex_street = '[\w( \-\.)?]+'
regex_city = '[\w( \-)?]+'
regex_size = '(small|normal|big)'
regex_weight = '[+-]?(\d*\.)?\d+'
regex_vehicle = '(car|foot|plane|rocket)'
regex_email = '[\w\d.+]+@[\w\d]+(?:\.[a-z]{2,4}){1,2}'
regex_password = '\w{8}'
regex_session_id = '[\w-]+'
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
syntax_update = [('packet_id', regex_id),
                 ('station', regex_city),
                 ('vehicle', regex_vehicle)]
syntax_delivered = [('packet_id', regex_id)]
syntax_add_user = [('email', regex_email),
                   ('name',regex_name),
                   ('street', regex_street),
                   ('zip', regex_zip), 
                   ('city', regex_city),
                   ('password', regex_password)]
syntax_authenticate_user = [('email', regex_email),
                            ('password', regex_password)]
syntax_update_user_adress = [('email', regex_email),
                             ('street', regex_street),
                             ('zip', regex_zip), 
                             ('city', regex_city),
                             ('session_id', regex_session_id)]
syntax_add_packet_to_user = [('email', regex_email),
                             ('packet', regex_id),
                             ('session_id', regex_session_id)]
syntax_get_packets_from_user = [('email', regex_email),
                                ('session_id', regex_session_id)]
syntax_delete_user = [('email', regex_email),
                      ('session_id', regex_session_id)]

def regex_matches_exactly(regex, string):
        compRegex = re.compile(regex)
        match = compRegex.match(string)
        return match != None and match.end() == len(string)
    
def get_first_not_contained(dic, req_list):
    for (key, value) in dic:
        if(not key in req_list):
            return key
    return None
    
def check_json_regex(dic, req_list):
    for (key, regex) in req_list:
        if(not key in dic):
            raise InvalidActionException(Exceptions.TYPE_KEY_NOT_FOUND, key, "Required key: "+key)
        elif(not regex_matches_exactly(regex, dic[key])):
            raise InvalidActionException(Exceptions.TYPE_INVALID_KEY, key, "Invalid value: "+dic[key]+" for key "+key)
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
