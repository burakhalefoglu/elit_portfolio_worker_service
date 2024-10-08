import os
import sys
from functools import wraps
from typing import Callable

from core.cross_cutting_concerns.cache.in_memory_cache import get_from_cache, set_cache
from kink import inject

from core.extensions.http_context.i_http_context import IHttpContext

@inject
def cache_aspect(func: Callable, http_context: IHttpContext = None):
    """
    :param http_context: dont inplement so it will inject
    :param func:
    :return:
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        file_paths = os.path.abspath(sys.modules[func.__module__].__file__).split("\\")
        service_name = file_paths[len(file_paths) - 3]
        params = {}
        for key in kwargs:
            for field in kwargs[key].__dataclass_fields__:
                value = getattr(kwargs[key], field)
                params[field] = value
        result = get_from_cache(service_name, http_context.get_uid() + str(params))
        if result is not None:
            return result
        else:
            out = await func(*args, **kwargs)
            if out is not None:
                set_cache(service_name, http_context.get_uid() +
                          str(params), out)
            return out

    return wrapper
