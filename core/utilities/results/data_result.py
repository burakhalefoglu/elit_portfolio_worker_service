from core.utilities.results.result import *


class DataResult(Result):
    def __init__(self, data: Any, message: str, success: bool, status_code: int):
        super(DataResult, self).__init__(
            data=data, message=message, success=success, status_code=status_code)


class ErrorDataResult(DataResult):
    def __init__(self, data: Any = None, message: str = None, status_code: int = 500):
        super(ErrorDataResult, self).__init__(
            data=data, message=message, success=False, status_code=status_code)


class SuccessDataResult(DataResult):
    def __init__(self, data: Any,  message: str = None, status_code: int = 200):
        super(SuccessDataResult, self).__init__(
            data=data, message=message, success=True, status_code=status_code)
