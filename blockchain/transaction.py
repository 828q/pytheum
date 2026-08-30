import hashlib
import json


class Transaction:
    def __init__(
        self,
        sender,
        public_key,
        recipient,
        amount,
        fee,
        nonce,
        chain_id,
    ):
        self.sender = sender
        self.public_key = public_key
        self.recipient = recipient
        self.amount = amount
        self.fee = fee
        self.nonce = nonce
        self.chain_id = chain_id
        self.signature = None

    def to_dict(self, include_signature=True):
        data = {
            "sender": self.sender,
            "public_key": self.public_key.hex(),
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.fee,
            "nonce": self.nonce,
            "chain_id": self.chain_id,
        }

        if include_signature:
            data["signature"] = self.signature

        return data

    def signing_bytes(self):
        data = self.to_dict(
            include_signature=False
        )

        encoded = json.dumps(
            data,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()

        return encoded

    def hash(self):
        return hashlib.sha256(
            self.signing_bytes()
        ).hexdigest()