from typing import List

from kink import inject
from starlette_context import context

from core.utilities.secrities.i_jwt_helper import IJWTHelper
from core.extensions.http_context.i_http_context import IHttpContext


@inject
class StarlatteHttpContext(IHttpContext):
    def __init__(self, jwt_helper: IJWTHelper):
        self.jwt_helper = jwt_helper

    def get_uid(self) -> str:
        token = context.data['Authorization']
        token_decoded = self.decode_token_without_verification(token)
        return token_decoded["sub"]

    def get_name(self) -> str:
        token = context.data['Authorization']
        token_decoded = self.decode_token_without_verification(token)
        return token_decoded["name"]

    def get_email(self) -> str:
        token = context.data['Authorization']
        token_decoded = self.decode_token_without_verification(token)
        return token_decoded["email"]

    def get_refresh_token(self) -> str:
        refresh_token = context.data['refresh_token']
        return refresh_token

    def get_oc(self) -> List[str]:
        pass
