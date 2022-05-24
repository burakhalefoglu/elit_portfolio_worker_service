from typing import Any, Optional, Union
from starlette.requests import HTTPConnection, Request
from starlette_context.plugins import Plugin


class RefreshTokenPlugin(Plugin):
    key = "refresh_token"

    async def process_request(
            self, request: Union[Request, HTTPConnection]
    ) -> Optional[Any]:
        raw_cookie = request.cookies.get("refresh_token")
        if not raw_cookie:
            return None

        return raw_cookie
