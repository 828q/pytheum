import hashlib
import json
import time


class Block:
    def __init__(
        self,
        height,
        previous_hash,
        transactions,
        validator,
        validator_public_key,
        validator_signature=None,
        timestamp=None,
    ):
        self.height = height
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.validator = validator
        self.validator_public_key = validator_public_key
        self.validator_signature = validator_signature
        self.timestamp = timestamp or time.time()

        self.block_hash = self.calculate_hash()

    def to_dict(self, include_signature=True):
        data = {
            "height": self.height,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "validator": self.validator,
            "validator_public_key": self.validator_public_key,
            "timestamp": self.timestamp,
        }

        if include_signature:
            data["validator_signature"] = self.validator_signature

        return data

    def signing_bytes(self):
        data = self.to_dict(
            include_signature=False
        )

        return json.dumps(
            data,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()

    def calculate_hash(self):
        block_data = self.signing_bytes()

        return hashlib.sha256(
            block_data
        ).hexdigest()

    def hash(self):
        return self.block_hash