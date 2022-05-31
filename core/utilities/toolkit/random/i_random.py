from abc import ABC, abstractmethod


class IRandom(ABC):
    @abstractmethod
    def create_random_hex_string(self, long: int):
        pass