"""
"""

import base64
import io
import random
import string
import unittest

import vcengine


class TestEncryptionEngine(unittest.TestCase):
    """
    Unit tests for vcengine.EncryptionEngine
    """
    def test_encrypt_str(self):
        with self.assertRaises(NotImplementedError):
            vcengine.EncryptionEngine().encrypt("rawr")

    def test_encrypt_list(self):
        with self.assertRaises(NotImplementedError):
            vcengine.EncryptionEngine().encrypt(["r", "a", "w", "r"])

    def test_decrypt_list(self):
        with self.assertRaises(NotImplementedError):
            vcengine.EncryptionEngine().decrypt(["r", "a", "w", "r"])

    def test_decrypt_str(self):
        with self.assertRaises(NotImplementedError):
            vcengine.EncryptionEngine().decrypt("rawr")


class TestPassThrough(unittest.TestCase):
    """
    Unit tests for vcengine.PassThrough
    """
    def setUp(self):
        self.test_strings = [
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(50, 200)))
            for n in range(random.randint(10, 50))
        ]

    def test_encrypt_str(self):
        fh = io.BytesIO()
        test_string = self.test_strings[0]
        vcengine.PassThrough().encrypt(test_string, fh)
        self.assertEqual(test_string, fh.get_value().decode())

    def test_encrypt_list(self):
        # Encrypt the list of strings into a single document.
        fh = io.BytesIO()
        vcengine.PassThrough().encrypt(self.test_strings, fh)
        # Get the encrypted document, split it on newline and compare.
        decrypted_strings = fh.get_value().decode().split("\n")
        self.assertEqual(self.test_strings, decrypted_strings)

    def test_decrypt_str(self):
        fh = io.BytesIO()
        test_string = self.test_strings[0]
        fh.write(bytes(test_string, "utf8"))
        decrypted_strings = []
        vcengine.PassThrough().decrypt(fh, decrypted_strings)
        self.assertEqual(test_string, decrypted_strings[0])

    def test_decrypt_list(self):
        # Write all test strings to the file handle, newline separated
        fh = io.BytesIO()
        fh.write(bytes("\n".join(self.test_strings), "utf8"))
        decrypted_strings = []
        # Decrypt the file handle into a list and compare
        vcengine.PassThrough().decrypt(fh, decrypted_strings)
        self.assertEqual(self.test_strings, decrypted_strings)


class TestBase64Engine(unittest.TestCase):
    """
    Unit tests for vcengine.Base64Engine
    """
    def setUp(self):
        self.test_strings = [
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(50, 200)))
            for n in range(random.randint(10, 50))
        ]

    def test_encrypt_str(self):
        fh = io.BytesIO()
        test_string = self.test_strings[0]
        vcengine.Base64Engine().encrypt(test_string, fh)
        encrypted_string = fh.get_value().decode()
        self.assertEqual(base64.b64encode(test_string), encrypted_string)

    def test_encrypt_list(self):
        fh = io.BytesIO()
        # Get a list of the encrypted strings
        vcengine.Base64Engine().encrypt(self.test_strings, fh)
        decrypted_strings = base64.b64decode(fh.get_value()).split("\n")
        self.assertEqual(self.test_strings, decrypted_strings)

    def test_decrypt_str(self):
        fh = io.BytesIO()
        test_string = self.test_strings[0]
        fh.write(base64.b64encode(bytes(test_string, "utf8")))
        decrypted_strings = []
        vcengine.Base64Engine().decrypt(fh, decrypted_strings)
        self.assertEqual(test_string, decrypted_strings[0])

    def test_decrypt_list(self):
        fh = io.BytesIO()
        fh.write(base64.b64encode(bytes("\n".join(self.test_strings), "utf8")))
        # Get a list of the decrypted strings
        decrypted_strings = []
        vcengine.Base64Engine().decrypt(fh, decrypted_strings)
        self.assertEqual(self.test_strings, decrypted_strings)
