
import sys
import unittest
import subprocess as sp

class TestVimcryptionVimscript(unittest.TestCase):
    """
    Unit tests for vimcryption.VCFileHandler
    """
    def setUp(self):
        os.remove("test/iopass_test.txt")
        os.remove("test/base64_test.txt")
        os.remove("test/viml_testlog.txt")

    def tearDown(self):
        os.remove("test/iopass_test.txt")
        os.remove("test/base64_test.txt")

    def test_vimscript(self):
        proc = sp.Popen(["vim -s test/test.viml"], shell=True)
        proc.wait()

        # Assert there was a zero return code
        self.assertEqual(proc.returncode, 0)

        # Check file output for plaintext
        with open("test/iopass_test.txt") as iop:
            self.assertEqual(iop.read(), "dmltY3J5cHRlZA==SU9QQVNTLOLOLOLOL\nLOLOLOLOL\n")

        # Check file output for plaintext
        with open("test/base64_test.txt") as b64:
            self.assertEqual(b64.read(), "dmltY3J5cHRlZA==QkFTRTY0ClJBV1JBV1JBV1JBV1JBV1IKUkFXUkFXUkFXUkFXUkFXUgo=")