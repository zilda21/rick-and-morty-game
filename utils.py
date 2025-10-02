import hmac, hashlib, secrets
def generate_key(): return secrets.token_hex(16)
def hmac_sha256(key, message): return hmac.new(key.encode(), str(message).encode(), hashlib.sha256).hexdigest()
def random_choice_secure(limit): return secrets.randbelow(limit)
