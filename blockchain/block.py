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
        timestamp=None,
    ):
        self.height = height
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.validator = validator
        self.timestamp = timestamp or time.time()

        # The hash is calculated once when the block is created.
        self.block_hash = self.calculate_hash()

    def to_dict(self):
        return {
            "height": self.height,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "validator": self.validator,
            "timestamp": self.timestamp,
        }

    def calculate_hash(self):
        block_data = json.dumps(
            self.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
        ).encode()

        return hashlib.sha256(block_data).hexdigest()

    def hash(self):
        return self.block_hash