import hashlib
import base64

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)
from cryptography.exceptions import InvalidSignature


class Wallet:
    def __init__(self):
        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def public_key_bytes(self):
        return self.public_key.public_bytes_raw()

    def address(self):
        digest = hashlib.sha256(
            self.public_key_bytes()
        ).digest()

        encoded = base64.b32encode(
            digest
        ).decode().rstrip("=")

        return "PY" + encoded[:32]

    def sign(self, message):
        if isinstance(message, str):
            message = message.encode()

        return self.private_key.sign(message).hex()

    @staticmethod
    def verify(public_key_bytes, message, signature):
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PublicKey,
        )

        if isinstance(message, str):
            message = message.encode()

        try:
            public_key = Ed25519PublicKey.from_public_bytes(
                public_key_bytes
            )

            public_key.verify(
                bytes.fromhex(signature),
                message,
            )

            return True

        except InvalidSignature:
            return False