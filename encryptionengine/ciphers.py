
from base64 import b64decode, b64encode
import binascii
import importlib

from engine import PassThrough
from base64engine import Base64Engine


class UnsupportedCipherException(Exception):
    pass


class NotVimcryptedException(Exception):
    pass


class CipherFactory:
    CIPHERS = {
        'IOPASS' : PassThrough, 
        'BASE64' : Base64Engine, 
        'AES128' : PassThrough, 
        'AES256' : PassThrough
    }

    def addCipher(self, cipher_token, cipher_engine):
        if cipher_token not in self.CIPHERS:
            if isinstance(cipher_engine, str):
                cipher_engine = importlib.import_module(cipher_engine)
            self.CIPHERS[cipher_token] = cipher_engine

    def getEngineForCipher(self, cipher_type, prompt=input):
        if cipher_type not in self.CIPHERS:
            raise UnsupportedCipherException("Tried to construct unsupported cipher: " + cipher_type)
        return self.CIPHERS[cipher_type](prompt=prompt, cipher_type=cipher_type)

    def getEngineForFile(self, file_handle, prompt=input):
        """ Process vimcryption header
            @param file_handle expects file-like bytes object
            0:15 (16)  bytes - b64encode of "vimcryption" if the file is our type
            16:23 (8)  bytes - b64encode of cipher, always 6 chars (AES128, AES256, BASE64, IOPASS)
            24:X  (X)  bytes - [optional]  - Engine may process additional metadata 
        """
        try:
            # First check to see if we should be handling it 
            header_valid = b64decode(file_handle.read(16))
            if (header_valid != b'vimcrypted'):
                raise NotVimcryptedException("Not a Vimcryption File Encoding")

            # Setup the cipher IO for encrypt/decrypt 
            cipher_type = b64decode(file_handle.read(8)).decode('utf-8')

            return self.getEngineForCipher(cipher_type, prompt=prompt)

        # Python2 Padding Error
        except TypeError as err:
            raise NotVimcryptedException("Not a Vimcryption File Encoding")

        # Python3 Padding Error 
        except binascii.Error as err:
            raise NotVimcryptedException("Not a Vimcryption File Encoding")

        # Unsupported Cipher
        except UnsupportedCipherException as err:
            print("Unsupported Cipher: " + self.cipher_type)
            raise NotVimcryptedException("Not a Vimcryption File Encoding")
