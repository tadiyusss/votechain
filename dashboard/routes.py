from . import dashboard
from flask import render_template, request
from .forms import *
from blockchain.transaction import Transaction
from blockchain.block import Block
from blockchain.blockchain import Blockchain
from blockchain.keys import Keys
from utils.users import User
import sqlite3
import os

blockchain = Blockchain()
keys = Keys()
user = User(sqlite3.connect("users.db", check_same_thread = False))

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
        return {
            "vote": form.candidates.data,
            "private_key": form.private_key.data
        }
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

@dashboard.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        if user.get_user_by_username(form.username.data):
            return "User already exists"
        generated_keys = keys.generate_keys()
        user.create_user(form.username.data, form.first_name.data, form.last_name.data, generated_keys["public_key"])
        return {
            "username": form.username.data,
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "public_key": generated_keys["public_key"],
            "private_key": generated_keys["private_key"]
        }
    return render_template('register.html', form = form)