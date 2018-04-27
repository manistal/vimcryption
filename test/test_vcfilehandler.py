"""
Unit tests for `VCFileHandler`
"""
# Standard Library
import sys
import unittest
from io import BytesIO


class VimMock(object):
    """ Mock class for the `vim` module.
    """
    def __init__(self):
        """ Mock `buffer` as a list.
        """
        self.buffer = list()

    @property
    def current(self):
        """ Mock `current` to return this object, so we can get at `buffer`.
        """
        return self

    def command(self, command):
        """ Short circuit mock for `command`.
        """
        pass

    def eval(self, command):
        """ Mock `eval` to always return "IOPASS".
        """
        return "IOPASS"


class TestVCFileHandler(unittest.TestCase):
    """ Unit tests for vimcryption.VCFileHandler
    """
    def setUp(self):
        """ Set up by instantiating a VCFileHandler and some known base64
            plaintext and ciphertext BytesIOs to use as mocked files.
        """
        # Mock Vim Library which doesnt exist outside vim
        sys.modules['vim'] = VimMock()

        # Set up the input
        import plugin.vimcryption as vimcryption
        self.vcf = vimcryption.VCFileHandler()
        self.plaintext_file = BytesIO(b'dmltY3J5cHRlZA==SU9QQVNT\nLOLPLAINTEXT\n')
        self.base64_file = BytesIO(b'dmltY3J5cHRlZA==QkFTRTY0CmxvbApsb2wKbG9sCgo=')

