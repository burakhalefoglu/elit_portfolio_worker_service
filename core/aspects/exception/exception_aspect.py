from core.cross_cutting_concerns.logger.logger import debug_logger
from core.utilities.custom_exceptions.custom_exceptions import SecurityException, \
    UnauthorizedAccessException, ValidationException
from functools import wraps
from core.utilities.messages.messages import DefaultErrorMessage
from core.utilities.results.result import ErrorResult


def exception_aspect(func):
    """

    :param func:
    :return:
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValidationException as e:
            return ErrorResult(e.message, status_code=400)

        except UnauthorizedAccessException as e:
            return ErrorResult(e.message, status_code=401)

        except SecurityException as e:
            return ErrorResult(e.message, status_code=403)

        except Exception as e:
            debug_logger.error(str(e), exc_info=True)
            return ErrorResult(DefaultErrorMessage)
            # return ErrorResult(str(e))
    return wrapper
