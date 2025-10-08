"""rsa tests"""

import unittest
from src.lab2 import rsa

class CalculatorTestCase(unittest.TestCase):
    """класс тестов"""

    def test_is_prime(self):
        """prime number"""
        self.assertEqual(rsa.is_prime(11), True)
    def test_is_not_prime(self):
        """not prime number"""
        self.assertEqual(rsa.is_prime(8), False)
    def test_gsd_not_one(self):
        """when gsd is not 1"""
        self.assertEqual(rsa.gcd(12, 15), 3)
    def test_gsd_one(self):
        """when gsd is 1"""
        self.assertEqual(rsa.gcd(3, 7), 1)
    def test_multiplicative_inverse(self):
        """multiplicative inverse"""
        self.assertEqual(rsa.multiplicative_inverse(7, 40), 23)
