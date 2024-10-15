from hashlib import sha256

class Block:
    def __init__(self, transactions: list, previous_block_hash: str = None, nonce: int = None, merkle_hash: str = None, block_hash: str = None) -> None:
        """
        Initialize the Block object. The block transactions must be a list of 8 transactions objects.
        Inputs:
            - transactions: List of transactions in the blocks that must be a power of 2
            - previous_block_hash: The hash of the previous block
            - nonce: The nonce of the block
        Output:
            - None            
        """
        self.transactions = transactions
        self.previous_block_hash = previous_block_hash
        self.nonce = nonce
        num_transactions = len(transactions)

        if num_transactions <= 0:
            raise ValueError("Invalid number of transactions in the block")
        if (num_transactions & (num_transactions - 1)) != 0:
            raise ValueError("Invalid number of transactions. The number of transactions must be a power of 2")
        
        for index in range(0, len(self.transactions)):
            transactions[index].index = index 

        if merkle_hash is not None:
            self.merkle_hash = merkle_hash
        else:
            self.merkle_hash = self.calculate_merkle_hash()

        if block_hash is not None:
            self.block_hash = block_hash
        else:
            self.block_hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the hash of the block
        Inputs:
            - None
        Outputs:
            - str: The hash of the block
        """
        self.block_hash = sha256(str(self.previous_block_hash).encode() + str(self.merkle_hash).encode()).hexdigest()
        return self.block_hash

    def calculate_merkle_hash(self) -> str:
        """
        Calculate the merkle hash of the transactions in the block and store it in the merkle_hash attribute
        Inputs:
            - None
        Outputs:
            - str: The merkle hash of the transactions in the block
        """
        def merkle_hash(transactions):
            if len(transactions) == 1:
                return transactions[0]
            new_level = []
            for i in range(0, len(transactions), 2):
                new_hash = sha256((transactions[i] + transactions[i + 1]).encode()).hexdigest()
                new_level.append(new_hash)
            return merkle_hash(new_level)
        
        transaction_hashes = [sha256(str(tx.hash).encode()).hexdigest() for tx in self.transactions]
        self.merkle_hash = merkle_hash(transaction_hashes)
        return self.merkle_hash
        
    def block_values(self) -> dict:
        """
        Returns the block's attributes in dictionary format
        Inputs:
            - None
        Outputs:
            - dict: The block's attributes
        """
        return {
            "transactions": [transaction for transaction in self.transactions],
            "previous_block_hash": self.previous_block_hash,
            "merkle_hash": self.merkle_hash,
            "block_hash": self.block_hash,
            "nonce": self.nonce
        }

    def calculate_nonce(self) -> int:
        """ 
        Calculate the nonce of the block
        Inputs:
            - None
        Outputs:
            - int: The nonce of the block
        """
        combined_hash = sha256(self.block_hash.encode() + self.previous_block_hash.encode() + self.merkle_hash.encode()).hexdigest()
        nonce = 0
        while True:
            nonce_hash = sha256(str(combined_hash + str(nonce)).encode()).hexdigest()
            if nonce_hash.startswith("0000"): # Difficulty level (more zeros = more difficulty)
                self.nonce = nonce
                return {
                    "nonce": nonce,
                    "block_hash": nonce_hash,
                    "result": nonce_hash
                }
            nonce += 1