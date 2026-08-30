from blockchain.chain import Blockchain
from blockchain.transaction import Transaction
from blockchain.wallet import Wallet


def test_transfer_updates_balances_and_nonce():
    chain = Blockchain(7770001)

    alice = Wallet()
    bob = Wallet()
    validator = Wallet()

    chain.create_account(alice.address(), 1000)
    chain.create_account(bob.address(), 500)
    chain.create_account(validator.address(), 0)

    transaction = Transaction(
        sender=alice.address(),
        public_key=alice.public_key_bytes(),
        recipient=bob.address(),
        amount=100,
        fee=1,
        nonce=0,
        chain_id=7770001,
    )

    transaction.signature = alice.sign(transaction.signing_bytes())

    assert chain.transfer(transaction, validator.address()) is True
    assert chain.get_account(alice.address()).balance == 899
    assert chain.get_account(bob.address()).balance == 600
    assert chain.get_account(validator.address()).balance == 1
    assert chain.get_account(alice.address()).nonce == 1
