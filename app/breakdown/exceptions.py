from ports.exceptions import NomadesExceptions


class BreakdownException(NomadesExceptions):
    """
    Base class for all breakdown exceptions
    """


class BreakdownNotFoundException(BreakdownException):
    """
    Exception raised when a breakdown is not found
    """
