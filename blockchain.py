import hashlib
import datetime
from colorama import init, Fore

init()


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.nonce = 0  # Nonce for mining
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(
            str(self.index).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8')
        )
        return sha.hexdigest()


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        # Generate a login transaction and add it to the blockchain
        transaction = Transaction(self.username, "System", "Login")
        blockchain.add_transaction(transaction)

    def logout(self):
        # Generate a logout transaction and add it to the blockchain
        transaction = Transaction(self.username, "System", "Logout")
        blockchain.add_transaction(transaction)


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.mining_reward = 5  # Reward for mining a block

    def create_genesis_block(self):
        transaction = Transaction("Genesis Block", "", "")
        return Block(0, datetime.datetime.now(), transaction, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        block = Block(len(self.chain), datetime.datetime.now(), transaction, self.get_latest_block().hash)
        self.chain.append(block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def mine_pending_transactions(self, miner):
        block = Block(len(self.chain), datetime.datetime.now(), self.pending_transactions, self.get_latest_block().hash)

        # Simulating the mining process by finding a hash with a certain number of leading zeros
        difficulty = 4
        while True:
            block.hash = block.calculate_hash()
            if block.hash.startswith('0' * difficulty):
                break
            block.nonce += 1

        self.chain.append(block)
        self.pending_transactions = []
        print(f"Block mined by {miner} with hash: {block.hash}")
        print(f"Mining reward of {self.mining_reward} units added to {miner}'s account.")

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def get_balance(self, user):
        balance = 0
        for block in self.chain:
            if isinstance(block.data, Transaction):
                if block.data.sender == user:
                    balance -= block.data.amount
                elif block.data.receiver == user:
                    balance += block.data.amount
        return balance


# Create a blockchain instance
blockchain = Blockchain()

# Create users
alice = User("Alice", "password123")
bob = User("Bob", "password456")

# Perform user login
alice.login()
bob.login()

# Print the blocks in the blockchain
for block in blockchain.chain:
    print(Fore.GREEN, "Block Index:", block.index)
    print("Timestamp:", block.timestamp)
    print("Data:", block.data.__dict__)
    print("Hash:", block.hash)
    print("Previous Hash:", block.previous_hash)
    print("--------------------")

# Perform user logout
alice.logout()

def get_user_login_status(username):
    login_status = False

    for block in blockchain.chain:
        if isinstance(block.data, Transaction) and block.data.sender == username and block.data.receiver == "System" and block.data.amount == "Login":
            login_status = True
        elif isinstance(block.data, Transaction) and block.data.sender == username and block.data.receiver == "System" and block.data.amount == "Logout":
            login_status = False

    return login_status


# Example usage
username = "Alice"
is_logged_in = get_user_login_status(username)

if is_logged_in:
    print(f"{Fore.RED} {username} is currently logged in.")
else:
    print(f"{Fore.RED} {username} is currently logged out.")

username = "Bob"
is_logged_in = get_user_login_status(username)

if is_logged_in:
    print(f"{Fore.RED} {username} is currently logged in.")
else:
    print(f"{Fore.RED} {username} is currently logged out.")

# Perform user logout
bob.logout()

# Print the blocks in the blockchain
for block in blockchain.chain:
    print(Fore.GREEN, "Block Index:", block.index)
    print("Timestamp:", block.timestamp)
    print("Data:", block.data.__dict__)
    print("Hash:", block.hash)
    print("Previous Hash:", block.previous_hash)
    print("--------------------")

# Example usage
username = "Alice"
is_logged_in = get_user_login_status(username)

if is_logged_in:
    print(f"{Fore.RED} {username} is currently logged in.")
else:
    print(f"{Fore.RED} {username} is currently logged out.")

username = "Bob"
is_logged_in = get_user_login_status(username)

if is_logged_in:
    print(f"{Fore.RED} {username} is currently logged in.")
else:
    print(f"{Fore.RED} {username} is currently logged out.")

# Define transactions between Alice and Bob
alice = "Alice"
bob = "Bob"
transaction1 = Transaction(alice, bob, 10)
transaction2 = Transaction(bob, alice, 5)

# Add the transactions to the pending transactions list
blockchain.add_transaction(transaction1)
blockchain.add_transaction(transaction2)

# Mine the pending transactions
miner = "Miner1"
blockchain.mine_pending_transactions(miner)

# Check the balance of Alice and Bob
alice_balance = blockchain.get_balance(alice)
bob_balance = blockchain.get_balance(bob)
print(f"Alice's Balance: {alice_balance}")
print(f"Bob's Balance: {bob_balance}")

# Check if the blockchain is valid
print("Is Blockchain Valid?", blockchain.is_chain_valid())
