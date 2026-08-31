import hashlib

from .block import Block
from .account import Account


BLOCK_REWARD = 10

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
        validator_public_key="",
        validator_signature=None,
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

    def stake(self, address, amount):
        account = self.get_account(address)

        if account is None:
            raise ValueError("Account does not exist")

        if amount <= 0:
            raise ValueError("Stake amount must be greater than zero")

        if account.balance < amount:
            raise ValueError("Insufficient balance for staking")

        account.balance -= amount
        account.staked_balance += amount

        return True

    def get_validators(self, minimum_stake=100):
        validators = []

        for account in self.accounts.values():
            if account.staked_balance >= minimum_stake:
                validators.append(account.address)

        return validators

    def select_validator(self, minimum_stake=100):
        validators = []

        for account in self.accounts.values():
            if account.staked_balance >= minimum_stake:
                validators.append(account)

        if not validators:
            raise ValueError("No eligible validators")

        validators.sort(
            key=lambda account: account.address
        )

        total_stake = sum(
            account.staked_balance
            for account in validators
        )

        previous_hash = self.latest_block().hash()

        seed = hashlib.sha256(
            previous_hash.encode()
        ).digest()

        number = int.from_bytes(
            seed,
            "big",
        )

        selection = number % total_stake

        current = 0

        for account in validators:
            current += account.staked_balance

            if selection < current:
                return account.address

        return validators[-1].address

    def reward_validator(self, validator, amount):
            account = self.get_account(validator)

            if account is None:
                raise ValueError(
                    "Validator account does not exist"
                )
                
            if amount <= 0:
                raise ValueError(
                    "Reward must be greater than zero"
                )
                
                account.balance += amount
                
                return True

    def produce_block(
        self,
        transactions,
        validator_wallet,
        minimum_stake=100,
    ):
        validator = self.select_validator(
            minimum_stake
        )

        if validator_wallet.address() != validator:
            raise ValueError(
                "Wallet does not belong to selected validator"
            )

        for transaction in transactions:
            self.transfer(
                transaction,
                validator,
            )
            
            self.reward_validator(
                validator,
                BLOCK_REWARD,
            )

        block = self.create_unsigned_block(
            [
                transaction.to_dict()
                for transaction in transactions
            ],
            validator,
            validator_wallet.public_key_bytes().hex(),
        )

        block.validator_signature = validator_wallet.sign(
            block.signing_bytes()
        )

        block.block_hash = block.calculate_hash()

        self.blocks.append(block)

        return block

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

    def create_unsigned_block(
        self,
        transactions,
        validator,
        validator_public_key,
    ):
        previous = self.latest_block()

        return Block(
            height=previous.height + 1,
            previous_hash=previous.hash(),
            transactions=transactions,
            validator=validator,
            validator_public_key=validator_public_key,
        )

    def add_block(
        self,
        transactions,
        validator,
        validator_public_key="",
        validator_signature=None,
    ):
        previous = self.latest_block()

        block = Block(
            height=previous.height + 1,
            previous_hash=previous.hash(),
            transactions=transactions,
            validator=validator,
            validator_public_key=validator_public_key,
            validator_signature=validator_signature,
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

            if not current.validator_public_key:
                return False

            if not current.validator_signature:
                return False

            import hashlib
            import base64
            
            digest = hashlib.sha256(
                bytes.fromhex(current.validator_public_key)
                ).digest()
                
            expected_validator = (
                "PY"
                + base64.b32encode(digest)
                .decode()
                .rstrip("=")[:32]
            )

            if expected_validator != current.validator:
                return False

            try:
                from cryptography.hazmat.primitives.asymmetric.ed25519 import (
                    Ed25519PublicKey,
                )

                public_key = Ed25519PublicKey.from_public_bytes(
                    bytes.fromhex(
                        current.validator_public_key
                    )
                )

                public_key.verify(
                    bytes.fromhex(
                        current.validator_signature
                    ),
                    current.signing_bytes(),
                )

            except Exception:
                return False

        return True