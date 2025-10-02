import hmac
import hashlib
import secrets


def generate_key() -> bytes:
    """Generate a secure 256-bit random key."""
    return secrets.token_bytes(32)


def secure_random(n: int) -> int:
    """Generate a secure random integer in [0, n-1]."""
    return secrets.randbelow(n)


def hmac_sha3_256(key: bytes, message: int) -> str:
    """Return HMAC-SHA3-256 of a message (Morty's number)."""
    return hmac.new(key, str(message).encode(), hashlib.sha3_256).hexdigest()
