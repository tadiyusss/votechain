from hashlib import sha256

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
        else:
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
            
            if current_block['previous_block_hash'] != previous_block['block_hash']:
                return False
            
            if nonce_hash.startswith("0000") == False:
                return False

            if current_block['block_hash'] != sha256(current_block['previous_block_hash'].encode() + current_block['merkle_hash'].encode()).hexdigest():
                return False

            level_one = [sha256(current_block['transactions'][i]['hash'].encode() + current_block['transactions'][i + 1]['hash'].encode()).hexdigest() for i in range(0, len(current_block['transactions']), 2)]
            level_two = [sha256(level_one[i].encode() + level_one[i + 1].encode()).hexdigest() for i in range(0, len(level_one), 2)]
            if sha256(level_two[0].encode() + level_two[1].encode()).hexdigest() != current_block['merkle_hash']:
                return False

        return True