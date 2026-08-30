from blockchain.wallet import Wallet
from blockchain.transaction import Transaction
from blockchain.chain import Blockchain


CHAIN_ID = 828


chain = Blockchain(CHAIN_ID)

alice = Wallet()
bob = Wallet()
validator = Wallet()


chain.create_account(
    alice.address(),
    1000,
)

chain.create_account(
    bob.address(),
    500,
)

chain.create_account(
    validator.address(),
    0,
)


transaction = Transaction(
    sender=alice.address(),
    public_key=alice.public_key_bytes(),
    recipient=bob.address(),
    amount=100,
    fee=1,
    nonce=0,
    chain_id=CHAIN_ID,
)


transaction.signature = alice.sign(
    transaction.signing_bytes()
)


print("=== BEFORE ===")

print(
    "Alice:",
    chain.get_account(alice.address()).balance,
    "PY",
)

print(
    "Bob:",
    chain.get_account(bob.address()).balance,
    "PY",
)

print(
    "Validator:",
    chain.get_account(validator.address()).balance,
    "PY",
)


chain.transfer(
    transaction,
    validator.address(),
)


print()
print("=== AFTER ===")

print(
    "Alice:",
    chain.get_account(alice.address()).balance,
    "PY",
)

print(
    "Bob:",
    chain.get_account(bob.address()).balance,
    "PY",
)

print(
    "Validator:",
    chain.get_account(validator.address()).balance,
    "PY",
)

print(
    "Alice nonce:",
    chain.get_account(alice.address()).nonce,
)

block = chain.add_block(
    [transaction.to_dict()],
    validator.address(),
)

print()
print("=== BLOCK ===")
print("Height:", block.height)
print("Previous hash:", block.previous_hash)
print("Hash:", block.hash())
print("Validator:", block.validator)

print()
print("=== CHAIN VALID ===")
print(chain.is_valid())