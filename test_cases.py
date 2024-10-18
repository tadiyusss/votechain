from block import Block
from transaction import Transaction
from blockchain import Blockchain
from datetime import datetime
import json
from sys import argv

blockchain = Blockchain()
names = ["Thaddeus", "Toledo"]
transactions = []
arguments = argv[1:]


# Create Transactions
if "--create-transactions" in arguments:
    for i in range(0, len(names)):
        timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        transaction = Transaction(names[i], index = i)
        transaction.transaction_hash = transaction.calculate_transaction_hash()
        transactions.append(transaction)

# Create Block
if "--create-block" in arguments:
    block = Block(transactions, "0", None, None, None, 0)
    block.root_hash = block.calculate_root_hash()
    block.block_hash = block.calculate_block_hash()
    block.nonce = block.calculate_block_nonce()

    blockchain.add_block(block)

    print(f"System Generated Chain Validity: {blockchain.validate_chain()}")

if "--export" in arguments:
    blockchain.export_chain()

# Load the chain from the database
if "--import" in arguments:
    blockchain.import_chain("blockchain")
    print(f"Database Generated Chain Validity: {blockchain.validate_chain()}")

