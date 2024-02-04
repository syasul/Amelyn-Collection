import os

class GenericUtils:
    @staticmethod
    def generateRandomHex(byteSize: int = 16):
        return os.urandom(byteSize).hex()
        