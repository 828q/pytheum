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

    def hash(self):
        block_data = {
            "height": self.height,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "validator": self.validator,
            "timestamp": self.timestamp,
        }

        encoded = json.dumps(
            block_data,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()

        return hashlib.sha256(encoded).hexdigest()

    def to_dict(self):
        return {
            "height": self.height,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "validator": self.validator,
            "timestamp": self.timestamp,
            "hash": self.hash(),
        }