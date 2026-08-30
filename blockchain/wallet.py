import hashlib
import base64

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)


class Wallet:
    def __init__(self):
        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def address(self):
        public_key_bytes = self.public_key.public_bytes_raw()

        digest = hashlib.sha256(public_key_bytes).digest()

        encoded = base64.b32encode(digest).decode().rstrip("=")

        return "PY" + encoded[:32]

    def sign(self, message):
        if isinstance(message, str):
            message = message.encode()

        return self.private_key.sign(message).hex()