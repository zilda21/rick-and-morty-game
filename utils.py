# utils.py
import hmac, hashlib, secrets

def generate_key():
    return secrets.token_hex(32)  # 256-bit key

def hmac_sha3_256(key, message):
    return hmac.new(key.encode(), str(message).encode(), digestmod=hashlib.sha3_256).hexdigest()

def secure_random(limit):
    return secrets.randbelow(limit)
