"""
"""

import base64
import io


class EncryptionEngine:
    """
    Base vimcryption encryption engine.
    """

    def __init__(self):
        pass

    def encrypt(self, data, fh):
        # type: (Union[List[str], str], io.BytesIO):
        raise NotImplementedError("IOBase.encrypt must be implemented by a derived class!")

    def decrypt(self, fh, data):
        # type: (io.BytesIO, Union[List[str], str]):
        raise NotImplementedError("IOBase.decrypt must be implemented by a derived class!")


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
            if line != "":
                data.append(line)


class Base64Engine(EncryptionEngine):
    """
    Simple base64 encode/decode engine.
      Base64 encodes 3 bytes of data into 4 6-bit characters.
      The 6-bit character set is typically A-Z, a-z, 0-9, +, and /.
      Data is padded with =.
    """
    encode_blocksize = 3  # In bytes
    decode_blocksize = 4  # In bytes

    @staticmethod
    def list_iter(data):
        #type: List[str]
        for line in data:
            for c in line:
                yield c
            yield "\n"

    @staticmethod
    def byte_iter(fh):
        # type: io.ByteIO
        c = fh.read(1)
        while c != b"":
            yield c
            c = fh.read(1)

    def encrypt(self, data, fh):
        # type: (Union[List[str], str], io.BytesIO):
        if isinstance(data, str):
            fh.write(base64.b64encode(data.encode("utf8")))
        else:
            # Initialize a buffer for block to encode
            block = ""
            for c in self.list_iter(data):
                block += c
                # When we reach the block size, encrypt the current
                # block as a string recursively and clear out block.
                if len(block) == self.encode_blocksize:
                    self.encrypt(block, fh)
                    block = ""
            self.encrypt(block, fh)

    def decrypt(self, fh, data):
        # type: (io.BytesIO, Union[List[str], str]):
        # Initialize buffers for the decoded line and the encoded block
        line = ""
        block = b""
        for b in self.byte_iter(fh):
            block += b
            # When we reach the block size, decode it and shove
            # the characters into our line.  Once we hit a the
            # end of a line, stick that guy into the list of
            # lines and clear it out.
            if len(block) == self.decode_blocksize:
                for c in base64.b64decode(block).decode():
                    if c == "\n":
                        data.append(line)
                        line = ""
                    else:
                        line += c
                block = b""
        # If there is a line left over, stick it in the list.
        if line != "":
            data.append(line)

if __name__ == "__main__":
    fh = io.BytesIO()
    engine = Base64Engine()
    engine.encrypt(["Rawr", "rAwr", "raWr", "rawR"], fh)
    print(fh.getvalue())
    print(base64.b64decode(fh.getvalue()))
    fh.seek(0)
    lines = []
    engine.decrypt(fh, lines)
    print(lines)
