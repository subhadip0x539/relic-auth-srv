from fastapi import status


class Error(Exception):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Internal Server Error"

    def __init__(self, message: str | None = None):
        self.message = message or self.message
        super().__init__(self.message)


class InvalidCredentialsError(Error):
    code = status.HTTP_401_UNAUTHORIZED
    message = "Invalid username or password"


class AccountLockedError(Error):
    code = status.HTTP_401_UNAUTHORIZED
    message = "Account temporarily locked. Try again later"
