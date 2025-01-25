import hashlib
import time
import json

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Include all block data in hash calculation
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty=4):
        # Simple proof-of-work: hash must start with specific number of zeros
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

class Blockchain:
    def __init__(self):
        # Create genesis block
        genesis_block = Block(0, [], '0')
        self.chain = [genesis_block]

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        new_block = Block(
            len(self.chain), 
            transactions, 
            self.get_latest_block().hash
        )
        new_block.mine_block()  # Optional proof-of-work
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Check current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check link to previous block
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

def main():
    # Blockchain demonstration
    blockchain = Blockchain()

    # Add some transactions
    blockchain.add_block(['zaif sends 1 BTC to Quadb'])
    blockchain.add_block(['Quadb sends 0.5 BTC to Charlie'])

    # Print blockchain details
    for block in blockchain.chain:
        print(f"\nBlock #{block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Transactions: {block.transactions}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Current Hash: {block.hash}")

    # Validate chain
    print(f"\nBlockchain Valid: {blockchain.is_chain_valid()}")

    # Tamper demonstration
    print("\n--- Tampering Demonstration ---")
    blockchain.chain[1].transactions = ['TAMPERED TRANSACTION']
    print(f"Blockchain Valid After Tampering: {blockchain.is_chain_valid()}")

if __name__ == "__main__":
    main()
