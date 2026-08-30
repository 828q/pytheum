from blockchain.wallet import Wallet
from blockchain.transaction import Transaction


CHAIN_ID = 828


alice = Wallet()
bob = Wallet()


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


print("Pytheum Started!")
print()

print("Alice:")
print(alice.address())

print()

print("Bob:")
print(bob.address())

print()

print("Transaction:")
print(transaction.to_dict())

print()

print("Transaction hash:")
print(transaction.hash())