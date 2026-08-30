from blockchain.wallet import Wallet
from blockchain.transaction import Transaction
from blockchain.chain import Blockchain


CHAIN_ID = 828


chain = Blockchain(CHAIN_ID)

alice = Wallet()
bob = Wallet()


chain.create_account(
    alice.address(),
    1000,
)

chain.create_account(
    bob.address(),
    500,
)


print("=== BEFORE ===")
print("Alice:", chain.get_account(alice.address()).balance, "PY")
print("Bob:", chain.get_account(bob.address()).balance, "PY")


transaction = Transaction(
    sender=alice.address(),
    recipient=bob.address(),
    amount=100,
    nonce=0,
    chain_id=CHAIN_ID,
)


transaction.signature = alice.sign(
    transaction.signing_bytes()
)


chain.transfer(
    transaction,
    alice,
)


print()
print("=== AFTER ===")
print("Alice:", chain.get_account(alice.address()).balance, "PY")
print("Bob:", chain.get_account(bob.address()).balance, "PY")
print("Alice nonce:", chain.get_account(alice.address()).nonce)