from functools import wraps
from core.cross_cutting_concerns.logger.logger import debug_logger, inform_logger


def debug_log_aspect(func):
    """

    :param func:
    :return:
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        out = await func(*args, **kwargs)
        debug_logger.debug("func ->  " + func.__name__ +
                           "; kwargs ->   " + str(kwargs) +
                           "; args ->  " + str(args) +
                           "; result -> " + str(out))
        return out

    return wrapper


def log_aspect(func):
    """

    :param func:
    :return:
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        out = await func(*args, **kwargs)
        inform_logger.info("func ->  " + func.__name__ +
                           "; kwargs ->   " + str(kwargs) +
                           "; args ->  " + str(args))
        return out

    return wrapper
