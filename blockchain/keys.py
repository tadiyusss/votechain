
from ecdsa import SigningKey, SECP256k1

class Keys:
    def __init__(self):
        pass

    def generate_keys(self) -> dict:
        private_key = SigningKey.generate(curve = SECP256k1)
        public_key = private_key.get_verifying_key()
        return {
            "private_key": private_key.to_string().hex(),
            "public_key": public_key.to_string().hex()
        }