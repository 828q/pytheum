from blockchain.wallet import Wallet


alice = Wallet()
bob = Wallet()

print("Pytheum Started!")
print()

print("Alice address:")
print(alice.address())

print()

print("Bob address:")
print(bob.address())

print()

message = "Hello Pytheum"

signature = alice.sign(message)

print("Alice signed a message.")
print("Signature:")
print(signature.hex())