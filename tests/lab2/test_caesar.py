"""caesar tests"""

import unittest
from src.lab2 import caesar

class CalculatorTestCase(unittest.TestCase):
    """класс тестов"""
    def test_encrypt_mixed_string(self):
        """test to check encrypting mixed string"""
        self.assertEqual(caesar.encrypt_caesar("Python3.6"), 'Sbwkrq3.6')
    def test_encrypt_null(self):
        """test to check encrypting null string"""
        self.assertEqual(caesar.encrypt_caesar(""), '')
    def test_decrypt_mixed_string(self):
        """test to check decrypting mixed string"""
        self.assertEqual(caesar.decrypt_caesar("Sbwkrq3.6"), 'Python3.6')
    def test_decrypt_null(self):
        """test to check decrypting null string"""
        self.assertEqual(caesar.decrypt_caesar(""), '')
