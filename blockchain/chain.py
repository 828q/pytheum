from .block import Block
from .account import Account

class Blockchain:
    def __init__(self):
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