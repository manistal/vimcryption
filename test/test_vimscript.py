
import os
import sys
import time
import unittest
import subprocess as sp

class TestVimcryptionVimscript(unittest.TestCase):
    """
    Integration testing for vimcryption vim plugin
    instantiates vim with plugin and runs commands 
    """

    @classmethod
    def setUpClass(cls):
        if os.path.exists("test/iopass_test.txt"):
            os.remove("test/iopass_test.txt")
        if os.path.exists("test/base64_test.txt"):
            os.remove("test/base64_test.txt")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("test/iopass_test.txt"):
            os.remove("test/iopass_test.txt")
        if os.path.exists("test/base64_test.txt"):
            os.remove("test/base64_test.txt")

    @unittest.skip("Currently failing in python 3 due to weird numpy import issue. #74")
    def test_vimscript(self):
        # Actual vim commands in viml script, pass them to Vim instance
        proc = sp.Popen(["vim -s test/test.viml"], shell=True)
        proc.wait()

        # Assert there was a zero return code
        self.assertEqual(proc.returncode, 0)

        # Check file output for plaintext
        with open("test/iopass_test.txt") as iop:
            self.assertEqual(iop.read(), "\nLOLOLOLOL\n")

        # Check file output for plaintext
        with open("test/base64_test.txt") as b64:
            self.assertEqual(b64.read(), "dmltY3J5cHRlZA==QkFTRTY0ClJBV1JBV1JBV1JBV1JBV1IK")
