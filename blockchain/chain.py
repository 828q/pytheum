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

    def transfer(self, transaction, sender_wallet):
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

        if sender.balance < transaction.amount:
            raise ValueError("Insufficient balance")

        if not transaction.signature:
            raise ValueError("Transaction is not signed")

        if transaction.sender != sender_wallet.address():
            raise ValueError("Wallet does not belong to sender")

        if not sender_wallet.verify(
            transaction.signing_bytes(),
            transaction.signature,
        ):
            raise ValueError("Invalid signature")

        sender.balance -= transaction.amount
        recipient.balance += transaction.amount

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