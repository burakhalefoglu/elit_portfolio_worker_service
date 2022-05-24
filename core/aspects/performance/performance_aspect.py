from functools import wraps
from datetime import datetime

from core.aspects.base.parametrized import __parametrized
from core.cross_cutting_concerns.logger.logger import debug_logger


@__parametrized
def performance_aspect(func, t: float):
    """

    :param func:
    :param t:
    :return:
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = datetime.now()
        out = await func(*args, **kwargs)
        end = datetime.now()
        dt = end - start
        if t <= dt.seconds:
            debug_logger.debug("func ->  " + func.__name__ +
                               "; kwargs ->   " + str(kwargs) +
                               "; args ->   " + str(args) +
                               "; expected_max_second: " + str(t) +
                               "; valid_second: " + "{:.12f}".format(dt.total_seconds()))
        return out

    return wrapper
