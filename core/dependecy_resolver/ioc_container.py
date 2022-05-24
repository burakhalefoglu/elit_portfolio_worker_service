from core.extensions.http_context.i_http_context import IHttpContext
from core.extensions.http_context.starlette.starlatte_http_context import StarlatteHttpContext
from core.utilities.ioc.punq.punq_module import PunqCoreModule
from core.utilities.secrities.i_jwt_helper import IJWTHelper
from core.utilities.secrities.jwt.jwt_helper import JWTHelper


def inject_dependencies():
    PunqCoreModule.add_dependencies_to_resolve(IJWTHelper, JWTHelper)
    PunqCoreModule.add_dependencies_to_resolve(IHttpContext, StarlatteHttpContext)