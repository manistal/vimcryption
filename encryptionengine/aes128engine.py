"""
Base64Engine
"""
from hashlib import sha1
import numpy as np

from .engine import BlockCipherEngine
from .aesutil import IncorrectPasswordException

__all__ = [
    "AES128Engine",
]


class AES128Engine(BlockCipherEngine):
    """
    Simple base64 encode/decode engine.
      Base64 encodes 3 bytes of data into 4 6-bit characters.
      The 6-bit character set is used is A-Z, a-z, + and /.
      Data is padded with =.
    """
    encrypt_blocksize = 128
    decrypt_blocksize = 128

    def readHeader(self, file_handle):
        self.cipher_key = file_handle.read(16)
        user_password = self.input("Enter password: ")
        user_pass_hash = sha1().update(user_password.encode('utf-8')).digest()
        
        if (user_pass_hash != self.cipher_key):
            raise IncorrectPasswordException("Wrong password!")

        self.generateRoundKeys()

    def writeHeader(self, file_handle):
        """
        Requires anyone implementing encryption Engine to 
        call super.writeHeader()
        """ 
        file_handle.seek(0) # Always start at the begginning
        file_handle.write(b64encode('vimcrypted'))
        file_handle.write(b64encode("AES128"))
        user_password = self.input("Enter password: ")
        file_handle.write(b64encode(user_password))

    def generateRoundKeys(self)
        key_matrix = self.textToMatrix(self.cipher_key)
        round_keys = [key_matrix]
        for round in range(1, 11):
            new_key_matrix = np.matrix(np.zeros((4, 4), dtype=int))
        

    @staticmethod
    def textToMatrix(text):
        matrix = np.matrix(np.zeros((4, 4), dtype=int))
        for col in range(0, 4):
            for row in range(0, 4):
                matrix[row, col] = ord(text[(col * 4) + row])
        return matrix

    @staticmethod
    def encrypt_block(block):
        return ""

    @staticmethod
    def decrypt_block(block):
        return ""
