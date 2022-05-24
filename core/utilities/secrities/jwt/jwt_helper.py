import os
import time
from typing import List, Any
import jwt
from datetime import datetime, timedelta

from dotenv import load_dotenv

from core.utilities.secrities.i_jwt_helper import IJWTHelper

load_dotenv()
secret_key = os.getenv('SECRET_KEY')


class JWTHelper(IJWTHelper):

    def validate_token(self, token: str):
        decoded_token = jwt.decode(
            token, secret_key, algorithms=["HS256"])
        return decoded_token if decoded_token["expires"] >= time.time() else None

    def decode_token_without_verification(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, options={
            "verify_signature": False})

    def create_token(self, model: dict, operation_claims: List[Any] = None) -> str:
        dt = datetime.utcnow() + timedelta(days=30)
        unix_time = int(time.mktime(dt.timetuple()))
        token = jwt.encode(
            {
                'sub': model["sub"],
                'name': model["name"],
                'email': model["email"],
                'ocs': operation_claims,
                "exp": unix_time
            },
            secret_key, algorithm="HS256"
        )
        return token
