"""
"""

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
        test_string = self.test_strings[0]
        self.assertEqual(test_string, vcengine.PassThrough().encrypt(test_string).next())

    def test_encrypt_list(self):
        # Get a list of the encrypted strings
        encrypted_strings = [item for item in vcengine.PassThrough().encrypt([s for s in self.test_strings])]
        self.assertEqual(self.test_strings, encrypted_strings)

    def test_decrypt_str(self):
        test_string = self.test_strings[0]
        self.assertEqual(test_string, vcengine.PassThrough().decrypt(test_string).next())

    def test_decrypt_list(self):
        # Get a list of the decrypted strings
        decrypted_strings = [item for item in vcengine.PassThrough().decrypt([s for s in self.test_strings])]
        self.assertEqual(self.test_strings, decrypted_strings)
