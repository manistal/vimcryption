"""
Contains Cipher factory and support classes and methods.
"""
# Standard Library
from base64 import b64decode
import binascii
import importlib
# Vimcryption
from .engine import PassThrough
from .base64engine import Base64Engine
from .aes128engine import AES128Engine


class UnsupportedCipherException(Exception):
    """ Exception type used to notify the system that the cipher mapping doesn't exist.
    """
    pass


class NotVimcryptedException(Exception):
    """ Exception type used to notify the system that a file is not vimcrypted.
    """
    pass


class CipherFactory(object):
    """ Factory class for `EncryptionEngine`s
    """
    CIPHERS = {
        'IOPASS' : PassThrough,
        'BASE64' : Base64Engine,
        'AES128' : AES128Engine,
        'AES256' : PassThrough
    }

    def add_cipher(self, cipher_token, cipher_engine):
        """ Adds a new `cipher_token` to `cipher_engine` mapping.
            `cipher_token` is a 6 character string.
            `cipher_engine` is a type that derives from EncryptionEngine.
        """
        if cipher_token not in self.CIPHERS:
            if isinstance(cipher_engine, str):
                cipher_engine = importlib.import_module(cipher_engine)
            self.CIPHERS[cipher_token] = cipher_engine

    def get_engine_for_cipher(self, cipher_type, prompt=input):
        """ Constructs and returns the EncryptionEngine for this `cipher_type`.
        """
        cipher_type = cipher_type.strip()  # Sanitize surrounding whitespace
        if cipher_type not in self.CIPHERS:
            raise UnsupportedCipherException("Tried to construct unsupported cipher: " + cipher_type)
        return self.CIPHERS[cipher_type](prompt=prompt)

    def get_engine_for_file(self, file_handle, prompt=input):
        """ Process vimcryption header
            @param file_handle expects file-like bytes object
            0:15 (16)  bytes - b64encode of "vimcryption" if the file is our type
            16:23 (8)  bytes - b64encode of cipher, always 6 chars (AES128, AES256, BASE64, IOPASS)
            24:X  (X)  bytes - [optional]  - Engine may process additional metadata
        """
        try:
            # First check to see if we should be handling it
            header_valid = b64decode(file_handle.read(16))
            if header_valid != b'vimcrypted':
                raise NotVimcryptedException("Not a Vimcryption File Encoding")

            # Setup the cipher IO for encrypt/decrypt
            cipher_type = b64decode(file_handle.read(8)).decode('utf-8')

            try:
                return self.get_engine_for_cipher(cipher_type, prompt=prompt)

            except UnsupportedCipherException:
                print("Unsupported Cipher: {}".format(cipher_type))
                raise NotVimcryptedException("Not a Vimcryption File Encoding")

        # Python2 Padding Error
        except TypeError:
            raise NotVimcryptedException("Not a Vimcryption File Encoding")

        # Python3 Padding Error
        except binascii.Error:
            raise NotVimcryptedException("Not a Vimcryption File Encoding")
