"""
AESEngine
"""
# Standard library
import hashlib
from base64 import b64encode
# site-packages
import numpy as np
# Vimcryption
from .engine import BlockCipherEngine
from .aesutil import IncorrectPasswordException
from .aesutil import aes_matrix, bytes_to_matrix, matrix_to_bytes
from .aesutil import AES_SBOX, AES_SBOX_INV, AES_RCON
from .aesutil import GMUL_BY2, GMUL_BY3, GMUL_BY9, GMUL_BY11, GMUL_BY13, GMUL_BY14


class AES128Engine(BlockCipherEngine):
    """ Simple base64 encode/decode engine.
        Base64 encodes 3 bytes of data into 4 6-bit characters.
        The 6-bit character set is used is A-Z, a-z, + and /.
        Data is padded with =.
    """
    encrypt_blocksize = 16
    decrypt_blocksize = 16
    pad_character = "\x00"

    def __init__(self, *args, **kwargs):
        super(AES128Engine, self).__init__(*args, **kwargs)
        self.round_keys = []

    def get_cipher_key(self):
        user_password = self.input("Enter password: ")
        return hashlib.pbkdf2_hmac('sha256', user_password.encode("utf8"), b'1', 10)

    def read_header(self, file_handle):
        header_key = file_handle.read(32)

        # Key is hashed securely! Compare against hash
        if hashlib.sha256(self.cipher_key).digest() != header_key:
            file_handle.seek(-32, 1)  # Reverse earlier file read back to where it was
            raise IncorrectPasswordException("Wrong password!")

        self.round_keys = AES128Engine.generate_round_keys(self.cipher_key)

    def write_header(self, file_handle):
        """ Requires anyone implementing encryption Engine to
            call super.writeHeader()
        """
        file_handle.seek(0) # Always start at the beginning
        file_handle.write(b64encode('vimcrypted'))
        file_handle.write(b64encode("AES128"))

        if self.cipher_key is None:
            self.cipher_key = self.get_cipher_key()

        # Don't write plain keys!! Hash them first!
        key_hash = hashlib.sha256(self.cipher_key).digest()
        file_handle.write(key_hash)

        self.round_keys = AES128Engine.generate_round_keys(self.cipher_key)

    @staticmethod
    def generate_round_keys(cipher_key):
        """ Generates and returns 11 round keys according to AES rules.
        """
        key_matrix = bytes_to_matrix(cipher_key)

        # 11 Rounds of Encryption
        # Round 0 = inKey
        round_keys = [key_matrix]

        # Round 1 - 10
        for current_round in range(1, 11):
            new_key_matrix = aes_matrix()
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
        """ XORs an AES state matrix with the current round key.
        """
        return np.bitwise_xor(state_matrix, round_key)

    @staticmethod
    def nibble_substitution(state_matrix):
        """ Does SBox substitution of each element of an AES state matrix.
        """
        sbox_substitute = np.vectorize(AES_SBOX.__getitem__)
        return sbox_substitute(state_matrix)

    @staticmethod
    def shift_rows(state_matrix):
        """ Rotates each row of an AES state matrix left by it's row number.
        """
        result_matrix = aes_matrix()  # Operation below is destructive!
        for row in range(0, 4):
            # *NOTE* NP defaults to backwards roll, need Forwards roll
            result_matrix[row, :] = np.roll(state_matrix[row].flat, -1 * row)
        return result_matrix

    @staticmethod
    def mix_column(column):
        """ Does Galois multiplication substitution of a column in an AES state matrix.
        """
        result_column = np.zeros((4, 1), dtype=int)
        result_column[0] = GMUL_BY2[column[0]] ^ GMUL_BY3[column[1]] ^          column[2]  ^          column[3]
        result_column[1] =          column[0]  ^ GMUL_BY2[column[1]] ^ GMUL_BY3[column[2]] ^          column[3]
        result_column[2] =          column[0]  ^          column[1]  ^ GMUL_BY2[column[2]] ^ GMUL_BY3[column[3]]
        result_column[3] = GMUL_BY3[column[0]] ^          column[1]  ^          column[2]  ^ GMUL_BY2[column[3]]
        return result_column

    @staticmethod
    def mix_columns(state_matrix):
        """ Mixes all columns of an AES state matrix.
        """
        result_matrix = aes_matrix()
        for column in range(0, 4):
            result_matrix[:, column] = AES128Engine.mix_column(state_matrix[:, column].flat)
        return result_matrix

    @staticmethod
    def nibble_substitution_inv(state_matrix):
        """ Inverse SBox substitution of each element of an AES state matrix.
        """
        sbox_substitute = np.vectorize(AES_SBOX_INV.__getitem__)
        return sbox_substitute(state_matrix)

    @staticmethod
    def shift_rows_inv(state_matrix):
        """ Inverse rotation of each row on an AES state matrix (rotate right by row number).
        """
        result_matrix = aes_matrix()  # Operation below is destructive!
        for row in range(0, 4):
            result_matrix[row, :] = np.roll(state_matrix[row].flat, row)
        return result_matrix

    @staticmethod
    def mix_column_inv(column):
        """ Inverse Galois multiplication substitution of a column in an AES state matrix.
        """
        result_column = np.zeros((4, 1), dtype=int)
        result_column[0] = GMUL_BY14[column[0]] ^ GMUL_BY11[column[1]] ^ GMUL_BY13[column[2]] ^  GMUL_BY9[column[3]]
        result_column[1] =  GMUL_BY9[column[0]] ^ GMUL_BY14[column[1]] ^ GMUL_BY11[column[2]] ^ GMUL_BY13[column[3]]
        result_column[2] = GMUL_BY13[column[0]] ^  GMUL_BY9[column[1]] ^ GMUL_BY14[column[2]] ^ GMUL_BY11[column[3]]
        result_column[3] = GMUL_BY11[column[0]] ^ GMUL_BY13[column[1]] ^  GMUL_BY9[column[2]] ^ GMUL_BY14[column[3]]
        return result_column

    @staticmethod
    def mix_columns_inv(state_matrix):
        """ Inverse column mixing of all columns of an AES state matrix.
        """
        result_matrix = aes_matrix()
        for column in range(0, 4):
            result_matrix[:, column] = AES128Engine.mix_column_inv(state_matrix[:, column].flat)
        return result_matrix

    def encrypt_block(self, block):
        """ 11 round AES block encryption.  Implements `BlockCipherEngine.encrypt_block` api.
        """
        state_matrix = bytes_to_matrix(block)

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

        return matrix_to_bytes(state_matrix)

    def decrypt_block(self, block):
        """ 11 round AES block decryption.  Implements `BlockCipherEngine.decrypt_block` api.
        """
        state_matrix = bytes_to_matrix(block)

        # Round 0 = Do the last stage of encryption backwards
        state_matrix = AES128Engine.add_round_key(state_matrix, self.round_keys[10])
        state_matrix = AES128Engine.shift_rows_inv(state_matrix)
        state_matrix = AES128Engine.nibble_substitution_inv(state_matrix)

        # Round 1 - 9 = AES
        for round_key in self.round_keys[9:0:-1]:
            state_matrix = AES128Engine.add_round_key(state_matrix, round_key)
            state_matrix = AES128Engine.mix_columns_inv(state_matrix)
            state_matrix = AES128Engine.shift_rows_inv(state_matrix)
            state_matrix = AES128Engine.nibble_substitution_inv(state_matrix)

        # Round 10 = No mixing
        state_matrix = AES128Engine.add_round_key(state_matrix, self.round_keys[0])

        return matrix_to_bytes(state_matrix).replace(self.pad_character, '')
