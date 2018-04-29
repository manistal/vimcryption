"""
Integration tests for the vimcryption plugin within vim.
"""
# Standard Library
import os
import sys
import time
import unittest
import subprocess as sp


TEST_DIR = os.path.dirname(__file__)
TEST_NAME_TEMPLATE = os.path.join(TEST_DIR, "{}_test.txt")

class TestVimcryptionVimscript(unittest.TestCase):
    """ Integration testing for vimcryption vim plugin
        instantiates vim with plugin and runs commands
    """

    @staticmethod
    def setUp():
        """ Clean up after interrupted previous runs. """
        TestVimcryptionVimscript.cleanUp()

    @staticmethod
    def tearDown():
        """ Clean up after testing. """
        TestVimcryptionVimscript.cleanUp()

    @staticmethod
    def cleanUp():
        """ Clear out any artifacts from testing. """
        for engine in ["iopass", "base64"]:
            test_name = TEST_NAME_TEMPLATE.format(engine)
            if os.path.exists(test_name):
                os.remove(test_name)

    def test_vimscript(self):
        """ Test `vim` by invoking vim with a script file that produces some artifact files
            that we can check.  Once the files are produced, check that the plaintext and
            ciphertext files have the expected contents.
        """
        # Actual vim commands in viml script, pass them to Vim instance
        proc = sp.Popen(["vim -s {}/test.viml".format(TEST_DIR)], shell=True)
        proc.wait()

        # Assert there was a zero return code
        self.assertEqual(proc.returncode, 0)

        # Check file output for plaintext
        with open(TEST_NAME_TEMPLATE.format("iopass")) as iop:
            self.assertEqual(iop.read(), "\nLOLOLOLOL\n")

        # Check file output for plaintext
        with open(TEST_NAME_TEMPLATE.format("base64")) as b64:
            self.assertEqual(b64.read(), "dmltY3J5cHRlZA==QkFTRTY0ClJBV1JBV1JBV1JBV1JBV1IK")
