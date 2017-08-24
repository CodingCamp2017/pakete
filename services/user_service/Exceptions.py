class InvalidActionException(Exception):
    pass

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