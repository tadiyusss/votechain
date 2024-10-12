from hashlib import sha256
import json
import sqlite3

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
        return self.chain[-1]['block_hash']

    def verify_block(self):
        """
        Will verify the following attributes of each block in the chain:
            - Previous block hash
            - Nonce
            - Block hash
            - Merkle hash
        Inputs:
            - None
        Outputs:
            - bool: True if the block is valid, False otherwise
        """
        for iterator in range(1, len(self.chain)):

            current_block = self.chain[iterator]
            previous_block = self.chain[iterator - 1]

            combined_hash = sha256((current_block['block_hash'] + current_block['previous_block_hash'] + current_block['merkle_hash']).encode()).hexdigest()
            nonce_hash = sha256(str(combined_hash + str(current_block['nonce'])).encode()).hexdigest()
            transaction_hashes = [transaction['hash'] for transaction in current_block['transactions']]

            while len(transaction_hashes) > 1:
                transaction_hashes = [sha256(transaction_hashes[i].encode() + transaction_hashes[i + 1].encode()).hexdigest() for i in range(0, len(transaction_hashes), 2)]
            
            if current_block['previous_block_hash'] != previous_block['block_hash']:
                return False
            
            if nonce_hash.startswith("0000000") == False:
                return False

            if current_block['block_hash'] != sha256(current_block['previous_block_hash'].encode() + current_block['merkle_hash'].encode()).hexdigest():
                return False

            if current_block['merkle_hash'] != transaction_hashes[0]:
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
            with open(f'{name}.json', 'w') as file:
                json.dump(self.chain, file, indent=4)

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