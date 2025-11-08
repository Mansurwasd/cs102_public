"""sudoku tests"""

import unittest
from src.lab3 import sudoku

class SudokuTestCase(unittest.TestCase):
    """класс тестов"""

    def test_group(self):
        """тест суммирования"""
        self.assertEqual(sudoku.group([1,2,3,4], 2), [[1, 2], [3, 4]])
        self.assertEqual(sudoku.group([1,2,3,4,5,6,7,8,9], 3), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])