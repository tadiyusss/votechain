from hashlib import sha256
from datetime import datetime

class Transaction:
    def __init__(self, data, timestamp = None, transaction_hash = None, index: int = None) -> None:
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
        self.index = index
        self.data = data
        self.timestamp = timestamp
        if transaction_hash is not None:
            self.hash = transaction_hash
        else:
            self.hash = self.calculate_hash()

        if timestamp is None:
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.timestamp = timestamp

    def calculate_hash(self) -> str:
        """
        Calculate the hash of the transaction using the data, timestamp, and previous block hash and store it in the hash attribute
        Inputs:
            - None
        Outputs:
            - str: The hash of the transaction
        """
        
        self.hash = sha256((str(self.index) + str(self.data) + str(self.timestamp)).encode()).hexdigest()
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