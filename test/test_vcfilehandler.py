"""
"""

import sys
import base64
import unittest
from io import BytesIO


class VimMock():
    def __init__(self):
        self.buffer = list()

    @property
    def current(self):
        return self

    def command(self, command):
        pass

    def eval(self, command):
        return "IOPASS"


class TestVCFileHandler(unittest.TestCase):
    """
    Unit tests for vimcryption.VCFileHandler
    """
    def setUp(self):
        # Mock Vim Library which doesnt exist outside vim
        sys.modules['vim'] = VimMock()

        # Set up the input
        import plugin.vimcryption as vimcryption 
        self.VCF = vimcryption.VCFileHandler() 
        self.plaintext_file = BytesIO(b'dmltY3J5cHRlZA==SU9QQVNT\nLOLPLAINTEXT\n')
        self.base64_file = BytesIO(b'dmltY3J5cHRlZA==QkFTRTY0CmxvbApsb2wKbG9sCgo=')

