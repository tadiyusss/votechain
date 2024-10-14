from hashlib import sha256
from datetime import datetime

class Transaction:
    def __init__(self, data, timestamp = datetime.now().strftime('%m/%d/%Y-%H:%M:%S:%f'), transaction_hash = None) -> None:
        """
        Initialize the Transaction object
        Inputs:
            - data: The data to be stored in the transaction
            - timestamp: The timestamp of the transaction
            - hash: The hash of the transaction
            - previous_block_hash: The hash of the previous block
        Outputs:
            - None
        """
        self.index = None
        self.data = data
        self.timestamp = timestamp
        if transaction_hash is not None:
            self.hash = transaction_hash
        else:
            self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the hash of the transaction using the data, timestamp, and previous block hash and store it in the hash attribute
        Inputs:
            - None
        Outputs:
            - str: The hash of the transaction
        """
        self.hash = sha256(str(self.index).encode() + str(self.data).encode() + str(self.timestamp).encode()).hexdigest()
        return self.hash

    def transaction_values(self) -> dict:
        """
        Return the transaction values in a dictionary format
        Inputs:
            - None
        Outputs:
            - dict: The transaction values in dictionary format
        """
        return {
            'index': self.index,
            'data': self.data,
            'timestamp': self.timestamp,
            'hash': self.hash
        }