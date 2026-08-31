class Account:
    def __init__(self, address, balance=0):
        self.address = address
        self.balance = balance
        self.nonce = 0
        self.staked_balance = 0

    def to_dict(self):
        return {
            "address": self.address,
            "balance": self.balance,
            "nonce": self.nonce,
            "staked_balance": self.staked_balance,
        }