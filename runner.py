from transaction import Transaction
from block import Block
from blockchain import Blockchain
import time
import json

blockchain = Blockchain()
transactions = []

for _ in range(2):
    transactions.append(Transaction(input("Enter Data: ")).transaction_values())

block = Block(transactions, blockchain.get_previous_block_hash())
block.calculate_nonce()
blockchain.add_block(block.block_values())
blockchain.output_chain()
print(f"Block validity: {blockchain.verify_block()}")