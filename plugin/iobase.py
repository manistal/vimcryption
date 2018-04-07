"""
"""


class IOBase:
    """
    Base vimcryption IO object.
    """

    def __init__(self):
        pass

    def encrypt(self, data):
        # type: (Union[List[str], str]) -> Union[List[str], str]:
        raise NotImplementedError("IOBase.encrypt must be implemented by a derived class!")

    def decrypt(self, data):
        # type: (Union[List[str], str]) -> Union[List[str], str]:
        raise NotImplementedError("IOBase.decrypt must be implemented by a derived class!")


class IOPassThrough:
    """
    Simple pass-through IO object.
    """
    def encrypt(self, data):
        # type: (Union[List[str], str]) -> Union[List[str], str]:
        return data

    def decrypt(self, data):
        # type: (Union[List[str], str]) -> Union[List[str], str]:
        return data
