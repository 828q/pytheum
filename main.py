from blockchain.wallet import Wallet
from blockchain.transaction import Transaction
from blockchain.chain import Blockchain


CHAIN_ID = 828


# Create the blockchain
chain = Blockchain(CHAIN_ID)


# Create wallets
alice = Wallet()
bob = Wallet()
validator = Wallet()


# Create accounts
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


# ============================================================
# TRANSACTION 1
# Alice sends Bob 100 PY
# Fee = 1 PY
# ============================================================

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


# Show balances before transaction 1
print("=== BEFORE TRANSACTION 1 ===")

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


# Process transaction 1
chain.transfer(
    transaction,
    validator.address(),
)


# Show balances after transaction 1
print()
print("=== AFTER TRANSACTION 1 ===")

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


# Create Block 1
block1 = chain.add_block(
    [transaction.to_dict()],
    validator.address(),
)


print()
print("=== BLOCK 1 ===")

print("Height:", block1.height)
print("Previous hash:", block1.previous_hash)
print("Hash:", block1.hash())
print("Validator:", block1.validator)


# ============================================================
# TRANSACTION 2
# Bob sends Alice 50 PY
# Fee = 1 PY
# ============================================================

transaction2 = Transaction(
    sender=bob.address(),
    public_key=bob.public_key_bytes(),
    recipient=alice.address(),
    amount=50,
    fee=1,
    nonce=0,
    chain_id=CHAIN_ID,
)

transaction2.signature = bob.sign(
    transaction2.signing_bytes()
)


# Process transaction 2
chain.transfer(
    transaction2,
    validator.address(),
)


# Create Block 2
block2 = chain.add_block(
    [transaction2.to_dict()],
    validator.address(),
)


print()
print("=== AFTER TRANSACTION 2 ===")

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
    "Bob nonce:",
    chain.get_account(bob.address()).nonce,
)


print()
print("=== BLOCK 2 ===")

print("Height:", block2.height)
print("Previous hash:", block2.previous_hash)
print("Hash:", block2.hash())
print("Validator:", block2.validator)


# ============================================================
# CHAIN VALIDATION
# ============================================================

print()
print("=== CHAIN VALID ===")

print(chain.is_valid())

print()
print("=== BAD SIGNATURE TEST ===")

bad_transaction = Transaction(
    sender=bob.address(),
    public_key=bob.public_key_bytes(),
    recipient=alice.address(),
    amount=25,
    fee=1,
    nonce=1,
    chain_id=CHAIN_ID,
)

# WRONG: Alice signs Bob's transaction
bad_transaction.signature = alice.sign(
    bad_transaction.signing_bytes()
)

try:
    chain.transfer(
        bad_transaction,
        validator.address(),
    )

    print("ERROR: Bad transaction was accepted!")

except ValueError as error:
    print("Rejected:", error)

print()
print("=== STAKING TEST ===")

chain.stake(
    alice.address(),
    500,
)

alice_account = chain.get_account(
    alice.address()
)

print(
    "Alice balance:",
    alice_account.balance,
    "PY",
)

print(
    "Alice staked:",
    alice_account.staked_balance,
    "PY",
)

print()
print("=== VALIDATORS ===")

validators = chain.get_validators()

for validator_address in validators:
    print(validator_address)

print()
print("=== POS VALIDATOR SELECTION ===")

selected = chain.select_validator()

print("Selected validator:", selected)