"""
"""

import base64
import io
import random
import string
import unittest

from plugin.engine import *


class TestEncryptionEngine(unittest.TestCase):
    """
    Unit tests for EncryptionEngine
    """
    def test_encrypt_str(self):
        with self.assertRaises(NotImplementedError):
            EncryptionEngine().encrypt("rawr", io.BytesIO())

    def test_encrypt_list(self):
        with self.assertRaises(NotImplementedError):
            EncryptionEngine().encrypt(["r", "a", "w", "r"], io.BytesIO())

    def test_decrypt_list(self):
        with self.assertRaises(NotImplementedError):
            EncryptionEngine().decrypt(io.BytesIO(), ["r", "a", "w", "r"])

    def test_decrypt_str(self):
        with self.assertRaises(NotImplementedError):
            EncryptionEngine().decrypt(io.BytesIO(), "rawr")


class TestPassThrough(unittest.TestCase):
    """
    Unit tests for PassThrough
    """
    def setUp(self):
        self.test_strings = [
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(50, 200)))
            for n in range(random.randint(10, 50))
        ]

    def test_encrypt_str(self):
        fh = io.BytesIO()
        test_string = self.test_strings[0]
        PassThrough().encrypt(test_string, fh)
        self.assertEqual(test_string, fh.getvalue().decode().rstrip("\n"))

    def test_encrypt_list(self):
        # Encrypt the list of strings into a single document.
        fh = io.BytesIO()
        PassThrough().encrypt(self.test_strings, fh)
        # Get the encrypted document, split it on newline and compare.
        decrypted_strings = fh.getvalue().decode().split("\n")
        if decrypted_strings[-1] == "":
            decrypted_strings.pop(-1)
        self.assertEqual(self.test_strings, decrypted_strings)

    def test_decrypt_str(self):
        fh = io.BytesIO()
        test_string = self.test_strings[0]
        fh.write(test_string.encode("utf8"))
        fh.seek(0)
        decrypted_strings = []
        PassThrough().decrypt(fh, decrypted_strings)
        self.assertEqual(test_string, decrypted_strings[0])

    def test_decrypt_list(self):
        # Write all test strings to the file handle, newline separated
        fh = io.BytesIO()
        fh.write("\n".join(self.test_strings).encode("utf8"))
        fh.seek(0)
        decrypted_strings = []
        # Decrypt the file handle into a list and compare
        PassThrough().decrypt(fh, decrypted_strings)
        self.assertEqual(self.test_strings, decrypted_strings)


class TestBase64Engine(unittest.TestCase):
    """
    Unit tests for Base64Engine
    """
    def setUp(self):
        self.test_strings = [
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(50, 200)))
            for n in range(random.randint(10, 50))
        ]

    def test_encrypt_str(self):
        fh = io.BytesIO()
        test_string = self.test_strings[0]
        Base64Engine().encrypt(test_string, fh)
        encrypted_string = fh.getvalue()
        self.assertEqual(base64.b64encode(test_string.encode("utf8")), encrypted_string)

    def test_encrypt_list(self):
        fh = io.BytesIO()
        # Get a list of the encrypted strings
        Base64Engine().encrypt(self.test_strings, fh)
        decrypted_strings = base64.b64decode(fh.getvalue()).decode().split("\n")
        if decrypted_strings[-1] == "":
            decrypted_strings.pop(-1)
        self.assertEqual(self.test_strings, decrypted_strings)

    def test_decrypt_str(self):
        fh = io.BytesIO()
        test_string = self.test_strings[0]
        fh.write(base64.b64encode(test_string.encode("utf8")))
        fh.seek(0)
        decrypted_strings = []
        Base64Engine().decrypt(fh, decrypted_strings)
        self.assertEqual(test_string, decrypted_strings[0])

    def test_decrypt_list(self):
        fh = io.BytesIO()
        fh.write(base64.b64encode("\n".join(self.test_strings).encode("utf8")))
        fh.seek(0)
        # Get a list of the decrypted strings
        decrypted_strings = []
        Base64Engine().decrypt(fh, decrypted_strings)
        self.assertEqual(self.test_strings, decrypted_strings)
