from typing import Any
from core.utilities.results.result import *


@dataclass
class DataResult(Result):
    def __init__(self, data: Any, message: str, success: bool, status_code: int):
        super(DataResult, self).__init__(
            data=data, message=message, success=success, status_code=status_code)


@dataclass
class ErrorDataResult(DataResult):
    def __init__(self, data=None, message: str = None, status_code: int = 500):
        super(ErrorDataResult, self).__init__(
            data=data, message=message, success=False, status_code=status_code)


@dataclass
class SuccessDataResult(DataResult):
    def __init__(self, data, message: str = None, status_code: int = 200):
        super(SuccessDataResult, self).__init__(
            data=data, message=message, success=True, status_code=status_code)
