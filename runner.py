from transaction import Transaction
from block import Block
from blockchain import Blockchain
from datetime import datetime
import time
import json
from sys import argv

blockchain = Blockchain()
data = ['Alice'] * 8


if '--export' in argv or '--both' in argv:
    transactions = [Transaction(data[i]) for i in range(0, len(data))]
    block = Block(transactions, blockchain.get_previous_block_hash())
    block.calculate_nonce()
    blockchain.add_block(block)
    print(f"Exported chain validity: {blockchain.verify_chain()}")
    blockchain.export_chain('blockchain.db')
if '--import' in argv or '--both' in argv:
    blockchain.import_chain('blockchain.db')
    print(f"Imported chain validity: {blockchain.verify_chain()}")
