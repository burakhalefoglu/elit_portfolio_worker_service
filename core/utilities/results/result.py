from dataclasses import dataclass
from typing import Any


@dataclass
class Result:
    data: Any
    message: str
    success: bool
    status_code: int


@dataclass
class ErrorResult(Result):
    def __init__(self, message: str = None, status_code: int = 500):
        super(ErrorResult, self).__init__(message=message,
                                          success=False, status_code=status_code, data=None)


@dataclass
class SuccessResult(Result):
    def __init__(self, message: str = None, status_code: int = 201):
        super(SuccessResult, self).__init__(
            message=message, success=True, status_code=status_code, data=None)
