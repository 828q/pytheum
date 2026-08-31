from blockchain.wallet import Wallet
from blockchain.transaction import Transaction
from blockchain.chain import Blockchain


CHAIN_ID = 828


# ============================================================
# CREATE BLOCKCHAIN
# ============================================================

chain = Blockchain(CHAIN_ID)


# ============================================================
# CREATE WALLETS
# ============================================================

alice = Wallet()
bob = Wallet()


# ============================================================
# CREATE ACCOUNTS
# ============================================================

chain.create_account(
    alice.address(),
    1000,
)

chain.create_account(
    bob.address(),
    500,
)


# ============================================================
# STAKE
# ============================================================

chain.stake(
    alice.address(),
    500,
)

chain.stake(
    bob.address(),
    200,
)


print("=== STAKING ===")

print(
    "Alice balance:",
    chain.get_account(alice.address()).balance,
    "PY",
)

print(
    "Alice staked:",
    chain.get_account(alice.address()).staked_balance,
    "PY",
)

print(
    "Bob balance:",
    chain.get_account(bob.address()).balance,
    "PY",
)

print(
    "Bob staked:",
    chain.get_account(bob.address()).staked_balance,
    "PY",
)


# ============================================================
# VALIDATORS
# ============================================================

print()
print("=== VALIDATORS ===")

validators = chain.get_validators()

for validator_address in validators:
    print(validator_address)


# ============================================================
# TRANSACTION 1
# Alice sends Bob 100 PY
# Fee = 1 PY
# ============================================================

transaction1 = Transaction(
    sender=alice.address(),
    public_key=alice.public_key_bytes(),
    recipient=bob.address(),
    amount=100,
    fee=1,
    nonce=0,
    chain_id=CHAIN_ID,
)

transaction1.signature = alice.sign(
    transaction1.signing_bytes()
)


print()
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


# ============================================================
# POS PRODUCES BLOCK 1
# ============================================================

selected_validator = chain.select_validator()

if selected_validator == alice.address():
    validator_wallet = alice
elif selected_validator == bob.address():
    validator_wallet = bob
else:
    raise ValueError("Validator wallet not found")

block1 = chain.produce_block(
    [transaction1],
    validator_wallet,
)


print()
print("=== BLOCK 1 ===")

print("Height:", block1.height)
print("Previous hash:", block1.previous_hash)
print("Hash:", block1.hash())
print("Validator:", block1.validator)

print(
    "Validator balance:",
    chain.get_account(
        block1.validator
    ).balance,
    "PY",
)


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
    "Alice nonce:",
    chain.get_account(alice.address()).nonce,
)


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


# ============================================================
# POS PRODUCES BLOCK 2
# ============================================================

selected_validator = chain.select_validator()

if selected_validator == alice.address():
    validator_wallet = alice
elif selected_validator == bob.address():
    validator_wallet = bob
else:
    raise ValueError("Validator wallet not found")

block2 = chain.produce_block(
    [transaction2],
    validator_wallet,
)

print()
print("=== BLOCK 2 ===")

print("Height:", block2.height)
print("Previous hash:", block2.previous_hash)
print("Hash:", block2.hash())
print("Validator:", block2.validator)


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
    "Bob nonce:",
    chain.get_account(bob.address()).nonce,
)


# ============================================================
# CHAIN VALIDATION
# ============================================================

print()
print("=== CHAIN VALID ===")

print(chain.is_valid())


# ============================================================
# BAD SIGNATURE TEST
# ============================================================

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


# Alice tries to sign Bob's transaction
bad_transaction.signature = alice.sign(
    bad_transaction.signing_bytes()
)


try:
    selected_validator = chain.select_validator()

    if selected_validator == alice.address():
        validator_wallet = alice
    elif selected_validator == bob.address():
        validator_wallet = bob
    else:
        raise ValueError("Validator wallet not found")

    chain.produce_block(
        [bad_transaction],
        validator_wallet,
    )

    print("ERROR: Bad transaction was accepted!")

except ValueError as error:
    print("Rejected:", error)