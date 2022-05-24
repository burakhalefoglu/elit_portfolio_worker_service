from functools import wraps
from cerberus import Validator

from core.aspects.base.parametrized import __parametrized
from core.utilities.custom_exceptions.custom_exceptions import ValidationException


@__parametrized
# https://cerberus-sanhe.readthedocs.io/usage.html
def validation_aspect(func, schema: dict):
    """

    :param func:
    :param schema:
    :return:
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        params = {}
        for key in kwargs:
            if type(kwargs[key]) == schema['type']:
                for field in kwargs[key].__dataclass_fields__:
                    value = getattr(kwargs[key], field)
                    params[field] = value
        v = Validator(schema['rules'])
        if v.validate(params) is False:
            raise ValidationException((str(v.errors)))
        else:
            return await func(*args, **kwargs)

    return wrapper
