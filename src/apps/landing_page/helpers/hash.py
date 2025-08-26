import hashlib


def hash(message: str) -> str:
    return hashlib.sha256(message.strip().encode()).hexdigest()
