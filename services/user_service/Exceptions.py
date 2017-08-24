TYPE_INVALID_KEY = "invalid key"
TYPE_KEY_NOT_FOUND = "key not found"
TYPE_NO_DATA_FOUND = "no data found"

class InvalidActionException(Exception):
    def __init__(self, exception_type, key, message):
        super(InvalidActionException, self).__init__(message)
        self.type = exception_type
        self.key = key
        
    
    def toDict(self):
        d = {"message":str(self), "type":self.type}
        if self.key != None:
            d["key"] = self.key
        return d

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