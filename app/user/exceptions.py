from ports.exceptions import NomadesExceptions


class UserException(NomadesExceptions):
    """
    Base class for User exceptions.
    """


class EmailAlreadyExists(UserException):
    pass
