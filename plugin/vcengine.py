"""
"""

import base64


class EncryptionEngine:
    """
    Base vimcryption encryption engine.
    """

    def __init__(self):
        pass

    def encrypt(self, data):
        # type: (Union[List[str], str]) -> Union[List[str], str]:
        raise NotImplementedError("IOBase.encrypt must be implemented by a derived class!")

    def decrypt(self, data):
        # type: (Union[List[str], str]) -> Union[List[str], str]:
        raise NotImplementedError("IOBase.decrypt must be implemented by a derived class!")


class PassThrough(EncryptionEngine):
    """
    Simple pass-through engine.
    """
    def encrypt(self, data):
        # type: (Union[List[str], str]) -> Union[List[str], str]:
        if isinstance(data, str):
            yield data
        else:
            for item in data:
                yield item

    def decrypt(self, data):
        # type: (Union[List[str], str]) -> Union[List[str], str]:
        if isinstance(data, str):
            yield data
        else:
            for item in data:
                yield item


class Base64Engine(EncryptionEngine):
    """
    Simple base64 encode/decode engine.
    """
    def encrypt(self, data):
        # type: (Union[List[str], str]) -> Union[List[str], str]:
        if isinstance(data, str):
            yield base64.b64encode(data)
        else:
            for item in data:
                yield base64.b64encode(item)

    def decrypt(self, data):
        # type: (Union[List[str], str]) -> Union[List[str], str]:
        if isinstance(data, str):
            yield base64.b64decode(data)
        else:
            for item in data:
                yield base64.b64decode(item)
