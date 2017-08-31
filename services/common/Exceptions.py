'''
Exception type of InvalidActionException: Indicates that a key has an invalid 
value (invalid format or content).
'''
TYPE_INVALID_KEY = "invalid key"

'''
Exception type of InvalidActionException: Indicates that a necessary key is missing.
'''
TYPE_KEY_NOT_FOUND = "key not found"

'''
Exception type of InvalidActionException: Indicates that the HTTP-Request contained
neither form nor json data.
'''
TYPE_NO_DATA_FOUND = "no data found"


'''
Exception that indicates that a request is malformed.
'''
class InvalidActionException(Exception):
    '''
    Creates a new InvalidActionException.
    exception_type: May be TYPE_INVALID_KEY, TYPE_KEY_NOT_FOUND or TYPE_NO_DATA_FOUND
    key: optional key, if not used set it to None
    message: a specific error message
    '''
    def __init__(self, exception_type, key, message):
        super(InvalidActionException, self).__init__(message)
        self.type = exception_type#The exception type
        self.key = key#Optional the key that is invalid/missing
        
    '''
    Returns a dictionary holding relevant data of this exception. This dict is
    intended to be send to the client for error resolving
    '''
    def toDict(self):
        d = {"message":str(self), "type":self.type}
        if self.key != None:
            d["key"] = self.key
        return d

'''
Exception that indicates that a request could not be commited because of an internal
error (e.g. kafka service not reachable)
str(self) will lead to more details
'''
class CommandFailedException(Exception):
    pass

class AuthenticationFailure(Exception):#
    pass

class UserExistsException(Exception):
    pass

class UserUnknownException(Exception):
    pass

class InvalidSessionIdException(Exception):
    pass

class SessionElapsedException(Exception):
    pass

class InvalidPasswortException(Exception):
    pass

class PacketNotFoundException(Exception):
    pass

class NoSessionIdException(Exception):
    pass

class NoPacketException(Exception):
    pass

class PacketAlreadyAddedException(Exception):
    pass

class NoSuchPacketAddedException(Exception):
    pass