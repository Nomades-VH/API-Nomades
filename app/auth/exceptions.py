from ports.exceptions import NomadesExceptions


class AuthException(NomadesExceptions):
    """Base class for exceptions in auth module."""


class InvalidCredentials(AuthException):
    """Raised when email or password are invalid."""


class InvalidToken(AuthException):
    """Raised when token is invalid."""
