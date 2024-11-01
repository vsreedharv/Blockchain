import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data_str = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(data_str.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 50

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, miner_address):
        block = Block(len(self.chain), self.get_latest_block().hash, time.time(), self.pending_transactions)
        block.mine_block(self.difficulty)
        self.chain.append(block)

        # Reward the miner
        self.pending_transactions = [{"from": None, "to": miner_address, "amount": self.mining_reward}]

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def get_balance_of_address(self, address):
        balance = 0
        for block in self.chain:
            if isinstance(block.data, list):  # skip genesis block
                for tx in block.data:
                    if tx["from"] == address:
                        balance -= tx["amount"]
                    if tx["to"] == address:
                        balance += tx["amount"]
        return balance

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# Creating and using the simple cryptocurrency
my_coin = Blockchain()

# Adding some transactions
my_coin.create_transaction({"from": "address1", "to": "address2", "amount": 100})
my_coin.create_transaction({"from": "address2", "to": "address1", "amount": 50})

# Mining pending transactions
print("Starting the miner...")
my_coin.mine_pending_transactions("miner_address")

print(f"Balance of miner_address is: {my_coin.get_balance_of_address('miner_address')}")

# Checking the balance
print(f"Balance of address1: {my_coin.get_balance_of_address('address1')}")
print(f"Balance of address2: {my_coin.get_balance_of_address('address2')}")

# Verifying blockchain validity
print("Blockchain valid?", my_coin.is_chain_valid())
