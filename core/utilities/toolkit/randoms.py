import string
import random


def create_random_hex_string(length: int):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
