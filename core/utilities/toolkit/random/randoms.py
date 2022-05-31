import string
import random

from core.utilities.toolkit.random.i_random import IRandom


class CoreRandom(IRandom):
    def create_random_hex_string(self, long: int):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(long))
