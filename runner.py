from transaction import Transaction
from block import Block
from blockchain import Blockchain
import time

blockchain = Blockchain()
datas = ['Bob', 'Alice', 'Eve', 'John']

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

print(f"Block validity: {blockchain.verify_block()}")