from core.utilities.messages.messages import SecurityMessage, UnauthorizedMessage, ValidationErrorMessage
from core.utilities.results.result import ErrorResult


class ValidationException(Exception):
    """Exception raised for errors in the input valdation.

    Attributes:
        message -- explanation of the error 
    """

    def __init__(self, message=ErrorResult(message=ValidationErrorMessage).__dict__):
        self.message = message
        super().__init__(self.message)


class UnauthorizedAccessException(Exception):
    """Exception raised for errors in the token valdation.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message=ErrorResult(message=UnauthorizedMessage).__dict__):
        self.message = message
        super().__init__(self.message)


class SecurityException(Exception):
    """Exception raised for errors in the autorize valdation.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message=ErrorResult(message=SecurityMessage).__dict__):
        self.message = message
        super().__init__(self.message)
