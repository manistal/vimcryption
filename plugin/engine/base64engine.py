"""
Base64Engine
"""

import base64

from .vcengine import BlockCipherEngine

__all__ = [
    "Base64Engine",
]


class Base64Engine(BlockCipherEngine):
    """
    Simple base64 encode/decode engine.
      Base64 encodes 3 bytes of data into 4 6-bit characters.
      The 6-bit character set is used is A-Z, a-z, + and /.
      Data is padded with =.
    """
    encrypt_blocksize = 3
    decrypt_blocksize = 4

    @staticmethod
    def encrypt_block(block):
        return base64.b64encode(block.encode("utf8"))

    @staticmethod
    def decrypt_block(block):
        return base64.b64decode(block).decode()
