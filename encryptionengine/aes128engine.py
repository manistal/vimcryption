"""
Base64Engine
"""
from hashlib import sha1
import numpy as np

from .engine import BlockCipherEngine
from .aesutil import *

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

    round_keys = []

    def readHeader(self, file_handle):
        cipher_key = file_handle.read(16)
        user_password = self.input("Enter password: ")
        user_pass_hash = sha1()
        user_pass_hash = user_pass_hash.update(user_password.encode('utf-8'))
        user_pass_hash = user_pass_hash.digest()
        
        if (user_pass_hash != cipher_key):
            raise IncorrectPasswordException("Wrong password!")

        self.generateRoundKeys(cipher_key)

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

    @staticmethod
    def generate_round_keys(cipher_key):
        key_matrix = bytesToMatrix(cipher_key)

        # 11 Rounds of Encyrption 
        # Round 0 = inKey
        round_keys = [key_matrix]

        # Round 1 - 10 
        for current_round in range(1, 11):
            new_key_matrix = AESMatrix()
            prev_round = round_keys[current_round - 1]

            # Column 0 = [Round - 1][Column 3] Transformed
            new_key_matrix[0, 0] = AES_RCON[current_round] ^ AES_SBOX[prev_round[1, 3]]
            new_key_matrix[1, 0] = AES_SBOX[prev_round[2, 3]] 
            new_key_matrix[2, 0] = AES_SBOX[prev_round[3, 3]]  
            new_key_matrix[3, 0] = AES_SBOX[prev_round[0, 3]]    

            # Column 0 ^= [Round - 1][SameCol] 
            for row in range(0, 4):
                new_key_matrix[row, 0] ^= prev_round[row, 0]

        
            # Column 1 - 3 = [Round - 1][SameCol] ^ [ThisRound][Col - 1]
            for column in range(1, 4):
                for row in range(0, 4):
                    new_key_matrix[row, column] = prev_round[row, column] ^ new_key_matrix[row, column - 1]

            round_keys.append(new_key_matrix)

        return round_keys

    @staticmethod
    def add_round_key(state_matrix, round_key):
        return np.bitwise_xor(state_matrix, round_key)

    @staticmethod
    def nibble_substitution(state_matrix):
        sbox_substitute = np.vectorize(AES_SBOX.__getitem__)
        return sbox_substitute(state_matrix)

    @staticmethod
    def shift_rows(state_matrix):
        result_matrix = AESMatrix()  # Operation below is destructive!
        for row in range(0, 4):
            # *NOTE* NP defaults to backwards roll, need Forwards roll
            result_matrix[row, :] = np.roll(state_matrix[row].flat, -1 * row)
        return result_matrix
    
    @staticmethod
    def mix_column(column):
        result_column = np.zeros((4, 1), dtype=int)
        result_column[0] = GMUL_BY2[column[0]] ^ GMUL_BY3[column[1]] ^          column[2]  ^          column[3]
        result_column[1] =          column[0]  ^ GMUL_BY2[column[1]] ^ GMUL_BY3[column[2]] ^          column[3]
        result_column[2] =          column[0]  ^          column[1]  ^ GMUL_BY2[column[2]] ^ GMUL_BY3[column[3]]
        result_column[3] = GMUL_BY3[column[0]] ^          column[1]  ^          column[2]  ^ GMUL_BY2[column[3]]
        return result_column

    @staticmethod
    def mix_columns(state_matrix):
        result_matrix = AESMatrix()
        for column in range(0, 4):
            result_matrix[:, column] = AES128Engine.mix_column(state_matrix[:, column].flat)
        return result_matrix

    def encrypt_block(self, block):
        state_matrix = bytesToMatrix(block)

        # Round 0 = Just add round key
        state_matrix = AES128Engine.add_round_key(state_matrix, self.round_keys[0])
        
        # Round 1 - 9 = AES
        for round_key in self.round_keys[1:10]:
            state_matrix = AES128Engine.nibble_substitution(state_matrix)
            state_matrix = AES128Engine.shift_rows(state_matrix)
            state_matrix = AES128Engine.mix_columns(state_matrix)
            state_matrix = AES128Engine.add_round_key(state_matrix, round_key)

        # Round 10 = No mixing
        state_matrix = AES128Engine.nibble_substitution(state_matrix)
        state_matrix = AES128Engine.shift_rows(state_matrix)
        state_matrix = AES128Engine.add_round_key(state_matrix, self.round_keys[10])

        return matrixToString(state_matrix)

    @staticmethod
    def decrypt_block(block):
        return ""
