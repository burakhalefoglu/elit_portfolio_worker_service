from abc import ABC, abstractmethod
from typing import Any, List


class IJWTHelper(ABC):

    @abstractmethod
    def validate_token(self, token: str):
        pass

    @abstractmethod
    def decode_token_without_verification(self, token: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def create_token(self, model: dict, operation_claims: List[Any] = None) -> str:
        pass
