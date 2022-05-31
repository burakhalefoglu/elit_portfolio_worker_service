from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from kink import inject

from core.utilities.secrities.i_jwt_helper import IJWTHelper


@inject
class JWTBearer(HTTPBearer):
    def __init__(self, jwt_helper: IJWTHelper):
        self.jwt_helper = jwt_helper
        super(JWTBearer, self).__init__(auto_error=True)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=401, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = self.jwt_helper.validate_token(jwtoken)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
