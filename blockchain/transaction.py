from hashlib import sha256
from datetime import datetime

class Transaction:
    def __init__(self, data = None, timestamp = None, transaction_hash = None, index = None) -> None:
        self.data = data
        self.index = index

        if timestamp is None:
            self.timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        else:
            self.timestamp = timestamp

        if transaction_hash is None:
            self.transaction_hash = self.calculate_transaction_hash()
        else:
            self.transaction_hash = transaction_hash

    def calculate_transaction_hash(self) -> None:
        data = (str(self.data) + str(self.timestamp) + str(self.index)).encode()
        return sha256(data).hexdigest()
    
    def transaction_values(self) -> dict:
        return self.__dict__