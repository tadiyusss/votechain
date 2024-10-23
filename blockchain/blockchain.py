from hashlib import sha256
import sqlite3
from blockchain.transaction import Transaction
from blockchain.block import Block

class Blockchain:
    
    def __init__(self) -> None:
        self.chain = []
    
    def add_block(self, block) -> None:
        self.chain.append(block)

    def get_next_index(self) -> int:
        return len(self.chain)
    
    def get_previous_block_hash(self) -> str:
        if len(self.chain) == 0:
            return "0"
        return self.chain[-1].block_hash

    def validate_chain(self) -> bool:
        for iterator in range(0, len(self.chain)):
            
            current_block = self.chain[iterator]
            previous_block = self.chain[iterator - 1]

            # Index   
            if current_block.index != iterator:
                print(f"Block {iterator} has an invalid index")
                return False

            # Previous block hash
            if current_block.previous_block_hash != previous_block.block_hash:
                if iterator != 0:
                    print(f"Block {iterator} has an invalid previous block hash")
                    return False

            # Current block hash    
            if current_block.block_hash != current_block.calculate_block_hash():
                print(f"Block {iterator} has an invalid block hash")
                return False
            
            # Root hash
            if current_block.root_hash != current_block.calculate_root_hash():
                print(f"Block {iterator} has an invalid root hash")
                return False

            # Nonce
            combined_hash = sha256(str(current_block.index).encode() + current_block.block_hash.encode() + current_block.previous_block_hash.encode() + current_block.root_hash.encode()).hexdigest()
            if sha256((combined_hash + str(current_block.nonce)).encode()).hexdigest().startswith("0" * 5) == False:
                print(f"Block {iterator} has an invalid nonce")
                return False

            # Transactions
            for transaction_iterator in range(0, len(current_block.transactions)):
                transaction = current_block.transactions[transaction_iterator]

                if transaction.index != transaction_iterator:
                    print(f"Block {iterator} has an invalid transaction index")
                    return False
                
                if transaction.validate_transaction() == False:
                    print(f"Block {iterator} has an invalid transaction")
                    return False
                
        return True

    def export_chain(self, filename = "blockchain"):
        connect = sqlite3.connect(f"{filename}.db")
        cursor = connect.cursor()

        # Drop the tables if they exist
        cursor.execute("DROP TABLE IF EXISTS blocks")
        cursor.execute("DROP TABLE IF EXISTS transactions")

        # Create the tables
        cursor.execute("CREATE TABLE IF NOT EXISTS `blocks` (`block_index` INT NOT NULL, `block_hash` VARCHAR(64) NOT NULL , `previous_block_hash` VARCHAR(64) NOT NULL , `root_hash` VARCHAR(64) NOT NULL , `nonce` INT NOT NULL );")
        """
        block_index INT NOT NULL,
        block_hash VARCHAR(64) NOT NULL,
        previous_block_hash VARCHAR(64) NOT NULL,
        root_hash VARCHAR(64) NOT NULL,
        nonce INT NOT NULL
        """
        cursor.execute("CREATE TABLE IF NOT EXISTS `transactions` (`transaction_index` INT NOT NULL , `data` VARCHAR(255) NOT NULL , `timestamp` VARCHAR(255) NOT NULL , `transaction_hash` VARCHAR(64) NOT NULL , `block_hash` VARCHAR(64) NOT NULL, `public_key` VARCHAR(128) NOT NULL, `signature` VARCHAR(128) NOT NULL );")
        """
        transaction_index INT NOT NULL,
        data VARCHAR(255) NOT NULL,
        timestamp VARCHAR(255) NOT NULL,
        transaction_hash VARCHAR(64) NOT NULL,
        block_hash VARCHAR(64) NOT NULL,
        public_key VARCHAR(128) NOT NULL,
        signature VARCHAR(128) NOT NULL
        """


        for chain in self.chain:
            block_values = chain.block_values()
            values = (block_values["index"], block_values["block_hash"], block_values["previous_block_hash"], block_values["nonce"], block_values["root_hash"])
            cursor.execute("INSERT INTO blocks (block_index, block_hash, previous_block_hash, nonce, root_hash) VALUES (?, ?, ?, ?, ?)", values)
            for transaction in block_values["transactions"]:
                values = (transaction["index"], transaction["data"], transaction["timestamp"], transaction["transaction_hash"], block_values["block_hash"], transaction["public_key"], transaction["signature"])
                cursor.execute("INSERT INTO transactions (transaction_index, data, timestamp, transaction_hash, block_hash, public_key, signature) VALUES (?, ?, ?, ?, ?, ?, ?)", values)
            cursor.execute("COMMIT;")
        connect.close()

    def import_chain(self, filename):
        self.chain = []
        connect = sqlite3.connect(f"{filename}.db")
        cursor = connect.cursor()

        cursor.execute("SELECT * FROM blocks ORDER BY block_index ASC")
        blocks = cursor.fetchall()
        for block in blocks:
            cursor.execute("SELECT * FROM transactions WHERE block_hash = ? ORDER BY transaction_index ASC", (block[1],))
            transactions = cursor.fetchall()
            transaction_objects = []
            for transaction in transactions:
                transaction_objects.append(Transaction(transaction[1], transaction[2], transaction[3], transaction[0], None, transaction[5], transaction[6]))
            block_object = Block(transaction_objects, block[2], block[4], block[3], block[1], block[0])
            self.add_block(block_object)
        connect.close()

    def view_transaction(self, block_hash, transaction_hash):
        # Slow, but it works hahaha
        # This is just for demonstration purposes
        for block in self.chain:
            if block.block_hash == block_hash:
                for transaction in block.transactions:
                    if transaction.transaction_hash == transaction_hash:
                        return transaction
        return None