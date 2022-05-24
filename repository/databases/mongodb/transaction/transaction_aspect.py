from functools import wraps
from core.aspects.base.parametrized import __parametrized


@__parametrized
def transaction_aspect(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        with mongodb_access.get_transaction_session_async() as s:
            async def cb():
                out = await func(*args, **kwargs)
                return out
            return s.with_transaction(cb)
    return wrapper
