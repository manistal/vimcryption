"""
Definitions of the base classes needed to match the EncryptionEngine API.
"""
# Standard Library
from base64 import b64encode
import functools


class EncryptionEngine(object):
    """ Base vimcryption encryption engine.
    """
    @staticmethod
    def buffer_iter(data):
        # type: List[str]
        """ Generative iterator that yields each character
            from a list of strings, joined by newlines.
        """
        for index, line in enumerate(data):
            for character in line:
                yield character
            if index < len(data):
                yield "\n"

    @staticmethod
    def byte_iter(file_handle):
        # type: io.ByteIO
        """ Generative iterator that yields each byte from a BytesIO object.
        """
        character = file_handle.read(1)
        while character != b"":
            yield character
            character = file_handle.read(1)

    def __init__(self, prompt=input):
        """ Sets the input method, cipher_type by classname and prompts for a key, if any.
        """
        self.input = prompt
        self.cipher_type = self.__class__.__name__[:6].upper()
        self.cipher_key = self.get_cipher_key()

    def get_cipher_key(self):
        """ Default cipher key is empty-string.
        """
        return ""

    def encrypt(self, data, file_handle):
        # type: (Union[List[str], str], io.BytesIO):
        """ `encrypt` must be implemented by derived classes.
        """
        raise NotImplementedError(self.__class__.__name__ + ".encrypt must be implemented by a derived class!")

    def decrypt(self, file_handle, data):
        # type: (io.BytesIO, Union[List[str], str]):
        """ `decrypt` must be implemented by derived classes.
        """
        raise NotImplementedError(self.__class__.__name__ + ".decrypt must be implemented by a derived class!")

    def encrypt_file(self, data, file_handle):
        # type: (Union[List[str], str], io.BytesIO)
        """ Convenience function for writing the header and encrypting the buffer at once.
        """
        self.write_header(file_handle)
        self.encrypt(data, file_handle)

    def decrypt_file(self, file_handle, data):
        # type: (io.BytesIO, Union[List[str], str])
        """ Convenience function for reading the header and decrypting the file at once.
        """
        self.read_header(file_handle)
        self.decrypt(file_handle, data)

    def read_header(self, file_handle):
        """ Implement for additional meta-data needed for the cipher implementation
        """
        pass

    def write_header(self, file_handle):
        """ Requires anyone implementing encryption Engine to
            call super.writeHeader()
        """
        file_handle.write(b64encode('vimcrypted'))
        file_handle.write(b64encode(self.cipher_type))


class PassThrough(EncryptionEngine):
    """ Simple pass-through engine.
    """
    def encrypt(self, data, file_handle):
        # type: (Union[List[str], str], io.BytesIO):
        if isinstance(data, str):
            file_handle.write((data + "\n").encode("utf8"))
        else:
            for item in data:
                file_handle.write((item + "\n").encode("utf8"))

    def decrypt(self, file_handle, data):
        # type: (io.BytesIO, Union[List[str], str]):
        line = ""
        for bchar in self.byte_iter(file_handle):
            char = ""
            try:
                char = bchar.decode("utf8")
            except UnicodeDecodeError:
                char = "?"

            if char == "\n":
                data.append(line)
                line = ""
            else:
                line += char

        if line != "":
            data.append(line)

    def write_header(self, file_handle):
        pass


class BlockCipherEngine(EncryptionEngine):
    """ Base class for block ciphers.  Provides generic API for common utilities.
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
    encrypt_blocksize = None
    decrypt_blocksize = None
    pad_character = None

    @staticmethod
    def block_iter(generator, block_size, pad):
        # type: (Iterable, int, Union[str, bytes])
        """ Generative iterator that yields a [byte] string of length `block_size`
            by concatenating characters yielded by `generator.  The final block
            is padded using `pad`.
        """
        block = []
        for item in generator:
            block.append(item)
            if len(block) == block_size:
                yield functools.reduce(lambda a, b: a + b, block)
                block = []
        if block:
            while len(block) < block_size:
                block.append(pad)
            yield functools.reduce(lambda a, b: a + b, block)

    def encrypt(self, data, file_handle):
        # type: (Union[Iterable[str], str], io.BytesIO)
        """ Block ciphers always encrypt blocks of a predefined size.  By default `encrypt` will consume
            `self.encrypt_blocksize` characters and call `self.encrypt_block` on that to determine what
            to write to `file_handle`.
            Derived classes are required to define `encrypt_blocksize` and define `encrypt_block`.
        """
        if isinstance(data, str):
            iterable = data
        else:
            iterable = self.buffer_iter(data)
        for block in self.block_iter(iterable, self.encrypt_blocksize, self.pad_character):
            file_handle.write(self.encrypt_block(block))

    def decrypt(self, file_handle, data):
        # type: (io.BytesIO, Union[Iterable[str], str])
        """ Block ciphers always decrypt blocks of a predefined size.  By default `decrypt` will consume
            `self.decrypt_blocksize` bytes and call `self.decrypt_block` on that to determine what
            to append to `data`.
            Derived classes are required to define `decrypt_blocksize` and define `decrypt_block`.
        """
        line = ""
        for block in self.block_iter(self.byte_iter(file_handle), self.decrypt_blocksize, self.pad_character.encode()):
            plaintext = self.decrypt_block(block)
            for character in plaintext:
                if character == "\n":
                    data.append(line)
                    line = ""
                else:
                    line += character
        if line != "":
            data.append(line)

    def encrypt_block(self, block):
        # type: (str)
        """ `encrypt_block` must be implemented by derived classes.
        """
        raise NotImplementedError(self.__class__.__name__ + ".encrypt_block must be implemented by a derived class!")

    def decrypt_block(self, block):
        # type: (bytes)
        """ `decrypt_block` must be implemented by derived classes.
        """
        raise NotImplementedError(self.__class__.__name__ + ".decrypt_block must be implemented by a derived class!")
