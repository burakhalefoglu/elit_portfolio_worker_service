from abc import ABC, abstractmethod
from typing import List


class IHttpContext(ABC):

    @abstractmethod
    def get_uid(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_email(self) -> str:
        pass

    @abstractmethod
    def get_refresh_token(self) -> str:
        pass

    @abstractmethod
    def get_oc(self) -> List[str]:
        pass
