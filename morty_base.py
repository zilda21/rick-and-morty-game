from utils import generate_key, hmac_sha256, secure_random

class MortyBase:
    """
    Default collaborative randomness:
    - commit(): publish HMAC(K2, m2)
    - pick_keep_index(r2, n_minus_one): returns (m2 + r2) % (N-1)
    - reveal(): returns (K2, m2) for verification
    Subclasses may override messages/behavior, but this satisfies the spec.
    """
    def __init__(self):
        self._k2 = None
        self._m2 = None
        self._commit = None

    def commit(self, n_minus_one: int) -> str:
        self._k2 = generate_key()
        self._m2 = secure_random(max(n_minus_one, 1))
        self._commit = hmac_sha256(self._k2, self._m2)
        return self._commit

    def pick_keep_index(self, r2: int, n_minus_one: int) -> int:
        if self._m2 is None:
            raise RuntimeError("Morty must commit() before pick_keep_index().")
        return (self._m2 + r2) % n_minus_one

    def reveal(self):
        if self._k2 is None or self._m2 is None:
            raise RuntimeError("Nothing to reveal; call commit() first.")
        return self._k2, self._m2
