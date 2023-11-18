from ports.exceptions import NomadesExceptions


class UserException(NomadesExceptions):
    """
    Base class for User exceptions.
    """
    message: str
    status_code: int = 400


class UserAlreadyExists(UserException):
    def __init__(self, *,  username: str):
        self.username = username
        self.message = f"Usuário com o username {username} já existe."
        super().__init__(self.message)


class EmailAlreadyExists(UserException):
    def __init__(self, *, email: str):
        self.email = email
        self.message = f"Usuário com o email {email} já existe."
        super().__init__(self.message)



