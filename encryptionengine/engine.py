"""
"""

from base64 import b64decode, b64encode
import binascii
from functools import reduce
import importlib


__all__ = [
    "EncryptionEngine",
    "PassThrough",
    "BlockCipherEngine",
]


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
        return self.CIPHERS[cipher_type](*args, prompt=prompt, cipher_type=cipher_type, **kwargs)

    def getEngineForFile(file_handle, prompt=input):
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


class EncryptionEngine:
    """
    Base vimcryption encryption engine.
    """

    def __init__(self, prompt=input, cipher_type=None):
        self.input = prompt
        self.cipher_type = cipher_type

    def encrypt(self, data, fh):
        # type: (Union[List[str], str], io.BytesIO):
        raise NotImplementedError("IOBase.encrypt must be implemented by a derived class!")

    def decrypt(self, fh, data):
        # type: (io.BytesIO, Union[List[str], str]):
        raise NotImplementedError("IOBase.decrypt must be implemented by a derived class!")

    def readHeader(self, file_handle):
        """
        Implement for additional meta-data needed for the cipher implementation
        """
        pass

    def writeHeader(self, file_handle):
        """
        Requires anyone implementing encryption Engine to 
        call super.writeHeader()
        """ 
        file_handle.seek(0) # Always start at the begginning
        file_handle.write(b64encode('vimcrypted'))
        file_handle.write(b64encode(self.cipher_type))


class PassThrough(EncryptionEngine):
    """
    Simple pass-through engine.
    """
    def encrypt(self, data, fh):
        # type: (Union[List[str], str], io.BytesIO):
        if isinstance(data, str):
            fh.write((data + "\n").encode("utf8"))
        else:
            for item in data:
                fh.write((item + "\n").encode("utf8"))

    def decrypt(self, fh, data):
        # type: (io.BytesIO, Union[List[str], str]):
        for bline in fh:
            line = bline.decode().rstrip("\n")
            data.append(line)

    def writeHeader(self, fh):
        pass


class BlockCipherEngine(EncryptionEngine):
    """
    Base class for block ciphers.  Provides generic API for common utilities.
        Derived classes MUST define `self.encrypt_blocksize` and `self.decrypt_blocksize`
        in order to use the default encrypt/decrypt functions.  Derived classes
        may implement `encrypt` and `decrypt` instead.
    Supplied methods:
        Buffer iterator generator function
        BytesIO iterator generator function
        Block iterator generator function
        `encrypt` based on Block iterator
        `decrypt` based on block iterator
    """
    @staticmethod
    def buffer_iter(data):
        #type: List[str]
        for i, line in enumerate(data):
            for c in line:
                yield c
            if i < len(data):
                yield "\n"

    @staticmethod
    def byte_iter(fh):
        # type: io.ByteIO
        c = fh.read(1)
        while c != b"":
            yield c
            c = fh.read(1)

    @staticmethod
    def block_iter(generator, block_size, pad):
        # type: (Iterable, int)
        block = []
        for item in generator:
            block.append(item)
            if len(block) == block_size:
                yield reduce(lambda a, b: a + b, block)
                block = []
        if len(block) > 0:
            while len(block) < block_size:
                block.append(pad)
            yield reduce(lambda a, b: a + b, block)

    def encrypt(self, data, fh):
        # type: (Union[Iterable[str], str], io.BytesIO)
        if isinstance(data, str):
            iterable = data
        else:
            iterable = self.buffer_iter(data)
        for block in self.block_iter(iterable, self.encrypt_blocksize, ""):
            fh.write(self.encrypt_block(block))

    def decrypt(self, fh, data):
        # type: (io.BytesIO, Union[Iterable[str], str])
        line = ""
        for block in self.block_iter(self.byte_iter(fh), self.decrypt_blocksize, b""):
            plaintext = self.decrypt_block(block)
            for c in plaintext:
                if c == "\n":
                    data.append(line)
                    line = ""
                else:
                    line += c
        if line != "":
            data.append(line)
