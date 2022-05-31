from kink import di

from core.extensions.http_context.i_http_context import IHttpContext
from core.extensions.http_context.starlette.starlatte_http_context import StarlatteHttpContext
from core.utilities.secrities.i_jwt_helper import IJWTHelper
from core.utilities.secrities.jwt.jwt_helper import JWTHelper
from core.utilities.toolkit.random.i_random import IRandom
from core.utilities.toolkit.random.randoms import CoreRandom


def inject_dependencies():
    di[IJWTHelper] = JWTHelper()
    di[IHttpContext] = StarlatteHttpContext()
    di[IRandom] = CoreRandom()