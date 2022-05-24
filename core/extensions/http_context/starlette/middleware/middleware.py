from starlette.middleware import Middleware
from starlette_context import plugins
from starlette_context.middleware import ContextMiddleware

from core.extensions.http_context.starlette.plugins.auth_context_plugin import AuthorizationPlugin
from core.extensions.http_context.starlette.plugins.session_plugin import RefreshTokenPlugin

context_middleware = Middleware(
        ContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            AuthorizationPlugin(),
            RefreshTokenPlugin(),
        )
    )
