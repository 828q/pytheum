from .block import Block
from .account import Account


class Blockchain:
    def __init__(self, chain_id):
        self.chain_id = chain_id
        self.blocks = []
        self.accounts = {}

        genesis = Block(
            height=0,
            previous_hash="0" * 64,
            transactions=[],
            validator="PYGENESIS",
        )

        self.blocks.append(genesis)

    def latest_block(self):
        return self.blocks[-1]

    def create_account(self, address, balance=0):
        if address in self.accounts:
            raise ValueError("Account already exists")

        account = Account(
            address=address,
            balance=balance,
        )

        self.accounts[address] = account

        return account

    def get_account(self, address):
        return self.accounts.get(address)

    def transfer(self, transaction, validator):
        if transaction.chain_id != self.chain_id:
            raise ValueError("Invalid chain ID")

        sender = self.get_account(transaction.sender)
        recipient = self.get_account(transaction.recipient)

        if sender is None:
            raise ValueError("Sender account does not exist")

        if recipient is None:
            raise ValueError("Recipient account does not exist")

        if transaction.nonce != sender.nonce:
            raise ValueError("Invalid nonce")

        if transaction.amount <= 0:
            raise ValueError("Amount must be greater than zero")

        if transaction.fee < 0:
            raise ValueError("Fee cannot be negative")

        if sender.balance < transaction.amount + transaction.fee:
            raise ValueError("Insufficient balance")

        if not transaction.signature:
            raise ValueError("Transaction is not signed")

        # Verify that the public key actually belongs
        # to the claimed sender address.
        import hashlib
        import base64

        digest = hashlib.sha256(
            transaction.public_key
        ).digest()

        expected_address = (
            "PY"
            + base64.b32encode(digest)
            .decode()
            .rstrip("=")[:32]
        )

        if expected_address != transaction.sender:
            raise ValueError(
                "Public key does not match sender"
            )

        # Verify the cryptographic signature.
        if not transaction.verify_signature():
            raise ValueError("Invalid signature")

        validator_account = self.get_account(validator)

        if validator_account is None:
            raise ValueError("Validator account does not exist")

        total_cost = transaction.amount + transaction.fee
        sender.balance -= total_cost
        recipient.balance += transaction.amount
        validator_account.balance += transaction.fee

        sender.nonce += 1

        return True

    def add_block(self, transactions, validator):
        previous = self.latest_block()

        block = Block(
            height=previous.height + 1,
            previous_hash=previous.hash(),
            transactions=transactions,
            validator=validator,
        )

        self.blocks.append(block)

        return block

    def is_valid(self):
        for i in range(1, len(self.blocks)):
            current = self.blocks[i]
            previous = self.blocks[i - 1]

            if current.previous_hash != previous.hash():
                return False

            if current.calculate_hash() != current.hash():
                return False

        return True