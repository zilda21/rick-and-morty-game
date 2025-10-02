# morty_base.py
from utils import generate_key, hmac_sha3_256, secure_random

class MortyBase:
    def __init__(self):
        pass

    # default probabilities; subclasses can override
    # stay = 1/N, switch = (N-1)/N if Morty never removes the gun
    def theoretical_probabilities(self, n: int):
        return 1.0 / n, (n - 1.0) / n
