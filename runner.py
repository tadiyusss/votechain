from block import Block
from transaction import Transaction
from blockchain import Blockchain
from datetime import datetime
import json
from sys import argv

blockchain = Blockchain()
names = ["Thaddeus", "Toledo"]

for counter in range(5):
    transactions = []
    for i in range(0, len(names)):
        transaction = Transaction(names[i], index = i)
        transactions.append(transaction)
    
    block = Block(transactions, blockchain.get_previous_block_hash(), None, index = blockchain.get_next_index())
    block.nonce = block.calculate_block_nonce()
    blockchain.add_block(block)

for block in blockchain.chain:
    print(json.dumps(block.block_values(), indent = 4))
print(f"System Generated Chain Validity: {blockchain.validate_chain()}")

blockchain.export_chain()
blockchain.import_chain("blockchain")
print(f"Database Generated Chain Validity: {blockchain.validate_chain()}")