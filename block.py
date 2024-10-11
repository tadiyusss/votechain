from hashlib import sha256

class Block:
    def __init__(self, transactions: list, previous_block_hash: str = None, nonce: int = None) -> None:
        """
        Initialize the Block object. The block transactions must be a list of 8 transactions objects.
        Inputs:
            - transactions: A list of 8 transaction objects
            - previous_block_hash: The hash of the previous block
            - nonce: The nonce of the block
        Output:
            - None            
        """
        if len(transactions) != 8:
            raise ValueError("Invalid number of transactions in block, expected 8")
        self.transactions = transactions
        self.nonce = nonce
        self.previous_block_hash = previous_block_hash
        self.merkle_hash = self.calculate_merkle_hash()
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

    def calculate_merkle_hash(self, block = None) -> str:
        """
        Calculate the merkle hash of the transactions in the block and store it in the merkle_hash attribute
        Inputs:
            - None
        Outputs:
            - str: The merkle hash of the transactions in the block
        """
        if block:
            return block
        level_one = [sha256(self.transactions[x]['hash'].encode() + self.transactions[x + 1]['hash'].encode()).hexdigest() for x in range(0, len(self.transactions), 2)]
        level_two = [sha256(level_one[x].encode() + level_one[x + 1].encode()).hexdigest() for x in range(0, len(level_one), 2)]
        return sha256(level_two[0].encode() + level_two[1].encode()).hexdigest()


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
            if nonce_hash.startswith("0000"):
                self.nonce = nonce
                return {
                    "nonce": nonce,
                    "block_hash": nonce_hash,
                    "result": nonce_hash
                }
            nonce += 1