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
                print(f"Block {iterator} has an invalid nonce")
                return False
            
            # Check if the transaction hashes are correct
            for transaction_iterator in range(0, len(current_block.transactions)):
                if current_block.transactions[transaction_iterator].calculate_hash() != current_block.transactions[transaction_iterator].hash:
                    print(f"Block {iterator}, transaction {transaction_iterator} has an invalid transaction hash")
                    return False
                
            # Check if the merkle hash is correct
            if current_block.calculate_merkle_hash() != current_block.merkle_hash:
                print(f"Calculated merkle hash: {current_block.calculate_merkle_hash()}")
                print(f"Saved merkle hash: {current_block.merkle_hash}")
                print(f"Block {iterator} has an invalid merkle hash")
                return False
            
            
        return True
    
    def export_chain(self, filetype = 'json', name = 'blockchain'):
        """
        Output the blockchain to a file
        Inputs:
            - filetype: [json, sqlite] The file type to output the blockchain to
        Outputs:
            - None
        """
        if filetype == "json":
            result = []
            for block in self.chain:
                block_values = block.block_values()
                result.append({
                    "block_hash": block_values['block_hash'],
                    "previous_block_hash": block_values['previous_block_hash'],
                    "merkle_hash": block_values['merkle_hash'],
                    "nonce": block_values['nonce'],
                    "transactions": [transaction.transaction_values() for transaction in block_values['transactions']]
                })
            with open(f'{name}.json', 'w') as file:
                json.dump({"blocks": result}, file, indent=4)

        elif filetype == "sqlite":

            conn = sqlite3.connect(f'{name}.db')
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS blocks (`block_hash` VARCHAR(64) NOT NULL,`previous_block_hash` VARCHAR(64) NOT NULL, `merkle_hash` VARCHAR(64) NOT NULL, `nonce` INT NOT NULL);")
            cursor.execute("CREATE TABLE IF NOT EXISTS `transactions` (`block_hash` VARCHAR(64) NOT NULL, `hash` VARCHAR(64) NOT NULL, `timestamp` VARCHAR(30) NOT NULL, `data` VARCHAR(255) NOT NULL );")

            for block in self.chain:
                sql = "INSERT INTO blocks (block_hash, previous_block_hash, merkle_hash, nonce) VALUES (?, ?, ?, ?)"
                cursor.execute(sql, (block['block_hash'], block['previous_block_hash'], block['merkle_hash'], block['nonce']))
                for transaction in block['transactions']:
                    sql = "INSERT INTO transactions (block_hash, hash, timestamp, data) VALUES (?, ?, ?, ?)"
                    cursor.execute(sql, (block['block_hash'], transaction['hash'], transaction['timestamp'], transaction['data']))
            cursor.execute("COMMIT;")
            cursor.close()

    def import_chain(self, filename):
        """
        Import a blockchain from a file
        Inputs:
            - filename: The name of the file to import the blockchain from
        Outputs:
            - None
        """
        extension = filename.split('.')[-1]
        if extension == "json":
            with open(filename, 'r') as file:
                blocks = json.load(file)['blocks']
                for block in blocks:
                    self.chain.append(Block(
                        [Transaction(transaction["data"], transaction["timestamp"], transaction["hash"]) for transaction in block['transactions']],
                        block["previous_block_hash"],
                        block["nonce"],
                        block["merkle_hash"],
                        block["block_hash"]
                    ))

        elif extension in ["sqlite3", "db"]:
            conn = sqlite3.connect(filename)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM blocks;")
            blocks = cursor.fetchall()
            for block in blocks:
                cursor.execute("SELECT hash, timestamp, data FROM transactions WHERE block_hash = ?", (block[0],))
                transactions = cursor.fetchall()
                # Add the block object to the chain with the transaction objects.
                self.chain.append(Block([Transaction(transaction[2], transaction[1], transaction[0]) for transaction in transactions], block[1], block[3], block[2], block[0]))