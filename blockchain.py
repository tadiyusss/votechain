"""
TODO:
- Fix import and export chain functions
"""

from hashlib import sha256
import json
import sqlite3
from block import Block
from transaction import Transaction

class Blockchain:
    
    def __init__(self):
        """
        Initialize the Blockchain object
        Inputs:
            - None
        Outputs:
            - None
        """
        self.chain = []

    def add_block(self, block) -> None:
        """
        TODO:
            - Must add validation before adding new block to the blockchain
            - The block must be valid
        Add a block to the blockchain
        Inputs:
            - block: The block object to be added to the blockchain
        Outputs:
            - None
        """ 
        self.chain.append(block)
    
    def get_previous_block_hash(self) -> str:
        """
        Get the hash of the previous block in the blockchain
        Inputs:
            - None
        Outputs:
            - str: The hash of the previous block
        """
        if len(self.chain) == 0:
            return "0"
        return self.chain[-1].block_hash

    def verify_chain(self):
        """
        Will verify the following attributes of each block in the chain:
            - Previous block hash
            - Nonce
            - Block hash
            - Transaction hashes (!)
            - Merkle hash
        Inputs:
            - None
        Outputs:
            - bool: True if the block is valid, False otherwise
        """
        
        for iterator in range(0, len(self.chain)):
            current_block = self.chain[iterator]
            previous_block = self.chain[iterator - 1]


            # Check if previous block hash is correct
            if current_block.previous_block_hash != previous_block.block_hash:
                if iterator != 0:
                    print(f"Block {iterator} has an invalid previous block hash")
                    return False
            
            # Check if the block hash is correct
            if current_block.calculate_hash() != current_block.block_hash:
                print(f"Block {iterator} has an invalid block hash")
                return False
            
            # Check if the nonce is correct
            combined_hash = sha256((current_block.block_hash + current_block.previous_block_hash + current_block.merkle_hash).encode()).hexdigest()
            if sha256(combined_hash.encode() + str(current_block.nonce).encode()).hexdigest()[:4] != "0000":
                print(current_block.block_hash, current_block.previous_block_hash, current_block.merkle_hash, current_block.nonce)
                print(f"Block {iterator} has an invalid nonce")
                return False
            
            # Check if the transaction hashes are correct
            for transaction_iterator in range(0, len(current_block.transactions)):
                if current_block.transactions[transaction_iterator].calculate_hash() != current_block.transactions[transaction_iterator].hash:
                    print(f"Block {iterator}, transaction {transaction_iterator} has an invalid transaction hash")
                    return False
                
            # Check if the merkle hash is correct
            if current_block.calculate_merkle_hash() != current_block.block_values()['merkle_hash']:
                print(f"Block {iterator} has an invalid merkle hash")
                print(f"Calulated merkle hash: {current_block.calculate_merkle_hash()}")
                print(f"Saved merkle hash: {current_block.merkle_hash}")
                return False
            
            
        return True
    
    def export_chain(self, filename = 'blockchain.db') -> None:
        """
        Export the chain into a db file
        Inputs:
            - filename: The name of the file to export the chain to
        Outputs:
            - File: The chain is exported into a db file
        """
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()

        # Drop the tables if they exist
        cursor.execute("DROP TABLE IF EXISTS blocks")
        cursor.execute("DROP TABLE IF EXISTS transactions")

        # Create the tables
        cursor.execute("CREATE TABLE IF NOT EXISTS `blocks` (`block_hash` VARCHAR(64) NOT NULL , `previous_block_hash` VARCHAR(64) NOT NULL , `merkle_hash` VARCHAR(64) NOT NULL , `nonce` INT NOT NULL );")
        cursor.execute("CREATE TABLE IF NOT EXISTS `transactions` (`transaction_index` INT NOT NULL , `data` VARCHAR(255) NOT NULL , `timestamp` VARCHAR(255) NOT NULL , `transaction_hash` VARCHAR(64) NOT NULL , `block_hash` VARCHAR(64) NOT NULL );")

        for block in self.chain:
            cursor.execute("INSERT INTO `blocks` (`block_hash`, `previous_block_hash`, `merkle_hash`, `nonce`) VALUES (?, ?, ?, ?);", (block.block_hash, block.previous_block_hash, block.merkle_hash, block.nonce))
            for transaction in block.transactions:
                cursor.execute("INSERT INTO `transactions` (`transaction_index`, `data`, `timestamp`, `transaction_hash`, `block_hash`) VALUES (?, ?, ?, ?, ?);", (transaction.index, transaction.data, transaction.timestamp, transaction.hash, block.block_hash))
        cursor.execute("COMMIT;")
        connection.close()

    def import_chain(self, filename = 'blockchain.db') -> None:
        """
        Import the chain from a db file
        Inputs:
            - filename: The name of the file to import the chain from
        Outputs:
            - None
        """
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()
        cursor.execute("SELECT block_hash, previous_block_hash, merkle_hash, nonce FROM blocks")
        blocks = cursor.fetchall()
        for block in blocks:
            cursor.execute("SELECT transaction_index, data, timestamp, transaction_hash FROM transactions WHERE block_hash = ? ORDER BY transaction_index", (block[0],))
            transactions = cursor.fetchall()
            transaction_objects = [Transaction(transaction[1], transaction[2], transaction[3], transaction[0]) for transaction in transactions]
            self.add_block(Block(transaction_objects, block[1], block[3], block[2], block[0]))
        connection.close()

