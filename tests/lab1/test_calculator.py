"""calculator tests"""

import unittest
from src.lab1 import calculator

class CalculatorTestCase(unittest.TestCase):
    """класс тестов"""

    def test_add(self):
        """тест суммирования"""
        self.assertEqual(calculator.add(1, -2), -1)
    def test_sub(self):
        """тест вычитания"""
        self.assertEqual(calculator.sub(1, -2), 3)
    def test_mul(self):
        """тест умножения """
        self.assertEqual(calculator.mul(1, -2), -2)
    def test_div0(self):
        """тест деления на 0"""
        self.assertEqual(calculator.div(1, 0), "Неправильный ввод")
    def test_div(self):
        """тест деления"""
        self.assertEqual(calculator.div(2, 2), 1)
    def test_pow(self):
        """тест возведения в степень"""
        self.assertEqual(calculator.power(2, 0), 1)
    def test_sqrt(self):
        """тест корня из числа"""
        self.assertEqual(calculator.sqrt(27, 3), 3)
