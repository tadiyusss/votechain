from transaction import Transaction
from block import Block
from blockchain import Blockchain
import time

blockchain = Blockchain()
datas = ['Bob', 'Alice', 'Eve', 'John', 'Doe', 'Jane', 'Smith', 'Johnson']

for i in range(25):
    transactions = []
    for data in datas:
        transaction = Transaction(data)
        transactions.append(transaction.transaction_values())

    start = time.time()
    block = Block(transactions, blockchain.get_previous_block_hash())
    print("Mining block...")
    block.calculate_nonce()

    blockchain.add_block(block.block_values())
    print(f"Time taken: {time.time() - start:.2f} seconds to mine {i + 1} block")

print("Blockchain:")
for block in blockchain.chain:
    print(f"Block Hash: {block['block_hash']}")
    print(f"Merkle Hash: {block['merkle_hash']}")
    print(f"Nonce: {block['nonce']}")
    print(f"Previous Block Hash: {block['previous_block_hash']}")
    for transaction in block['transactions']:
        print(transaction)
    print("-" * 50)

print(f"Block validity: {blockchain.verify_block()}")