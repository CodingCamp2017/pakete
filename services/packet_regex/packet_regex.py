from Exceptions import InvalidActionException
import re
import json

regex_name = '[\w ]+'
regex_id = '[\w-]+'
regex_zip = '\\d{5}'
regex_street = '[\w( \-\.)?]+'
regex_city = '[\w( \-)?]+'
regex_size = '(small|normal|big)'
regex_weight = '[+-]?(\\d*\\.)?\\d+'
regex_vehicle = '(car|foot|plane|rocket)'
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

def regex_matches_exactly(regex, string):
        compRegex = re.compile(regex)
        match = compRegex.match(string)
        return match != None and match.end() == len(string)
    
def check_json_regex(dic, req_list):
    for (key, regex) in req_list:
        if(not key in dic):
            raise InvalidActionException("Required key: "+key)
        elif(not regex_matches_exactly(regex, dic[key])):
            raise InvalidActionException("Invalid value: "+dic[key]+" for key "+key)
    if(len(dic) != len(req_list)):
        raise InvalidActionException("Unknown keys in "+json.dumps(dic))
        
        
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
