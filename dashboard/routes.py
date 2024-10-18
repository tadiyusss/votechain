from . import dashboard
from flask import render_template, request
from .forms import VoteForm
from blockchain.transaction import Transaction
from blockchain.block import Block
from blockchain.blockchain import Blockchain
import os

blockchain = Blockchain()
if os.path.isfile("blockchain.db"):
    blockchain.import_chain("blockchain")

@dashboard.route('/', methods = ['GET', 'POST'])
def index():
    form = VoteForm()
    if request.method == "POST" and form.validate_on_submit():
        transaction = Transaction(form.candidates.data, index = 0)
        block = Block([transaction], blockchain.get_previous_block_hash(), None, index = blockchain.get_next_index())
        block.nonce = block.calculate_block_nonce()
        blockchain.add_block(block)
        if blockchain.validate_chain():
            blockchain.export_chain("blockchain")

    return render_template('vote.html', form = form, is_valid = blockchain.validate_chain())

@dashboard.route('/view_results')
def results():
    results = {}
    for block in blockchain.chain:
        for transaction in block.transactions:
            if transaction.data in results:
                results[transaction.data] += 1
            else:
                results[transaction.data] = 1
    return render_template('results.html', results = results, is_valid = blockchain.validate_chain())