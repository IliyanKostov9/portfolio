import hashlib
from typing import Final

from django.core.cache import caches
from django.core.signing import BadSignature, TimestampSigner

MAX_AGE: Final[int] = 7200


class SecurityManager:
    @staticmethod
    def _key(token: str) -> str:
        return "invalid_token:" + hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def generate_token(email: str) -> str:
        return TimestampSigner().sign(email)

    @staticmethod
    def verify_token(token: str, email: str) -> bool:
        if caches["tokens"].get(SecurityManager._key(token)):
            return False

        try:
            signed_email: str = TimestampSigner().unsign(token, max_age=7200)
        except BadSignature:
            return False

        return signed_email == email

    @staticmethod
    def invalidate(token: str) -> None:
        caches["tokens"].set(SecurityManager._key(token), True, timeout=MAX_AGE)
