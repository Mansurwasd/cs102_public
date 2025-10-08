"""vigenere tests"""

import unittest
from src.lab2 import vigenre

class CalculatorTestCase(unittest.TestCase):
    """класс тестов"""
    def test_encrypt_different_string(self):
        """test to check encrypting string with different amount of letters"""
        self.assertEqual(vigenre.encrypt_vigenere("ATTACKATDAWN", "LEMON"), 'LXFOPVEFRNHR')
    def test_encrypt_string(self):
        """test to check encrypting string"""
        self.assertEqual(vigenre.encrypt_vigenere("PYTHON", "A"), 'PYTHON')
    def test_decrypt_string(self):
        """test to check decrypting string"""
        self.assertEqual(vigenre.decrypt_vigenere("PYTHON", "A"), 'PYTHON')
    def test_decrypt_null(self):
        """test to check decrypting string with different amount of letters"""
        self.assertEqual(vigenre.decrypt_vigenere("LXFOPVEFRNHR", "LEMON"), 'ATTACKATDAWN')
