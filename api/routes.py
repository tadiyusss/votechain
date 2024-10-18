from . import api
from flask import render_template
from blockchain.blockchain import Blockchain
from blockchain.block import Block
from blockchain.transaction import Transaction
import os

blockchain = Blockchain()

if os.path.isfile("blockchain.db"):
    blockchain.import_chain("blockchain")

@api.route('/view_chain')
def view_chain():
    chain = {"blocks": []}
    for block in blockchain.chain:
        chain["blocks"].append(block.block_values())
    return chain