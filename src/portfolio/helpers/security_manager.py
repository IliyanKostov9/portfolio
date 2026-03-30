from django.core.signing import TimestampSigner


class SecurityManager:
    @staticmethod
    def generate_token(email: str) -> str:
        signer = TimestampSigner()
        token = signer.sign(email)

        return token

    @staticmethod
    def verify_token(token: str) -> bool:
        signer = TimestampSigner()
        try:
            signer.unsign(token, max_age=7200)
            return True
        except Exception:
            pass
        return False
