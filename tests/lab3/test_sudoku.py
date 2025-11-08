"""sudoku tests"""

import unittest
from src.lab3 import sudoku


class SudokuTestCase(unittest.TestCase):
    """класс тестов"""

    def test_group(self):
        """group function test"""
        self.assertEqual(sudoku.group([1,2,3,4], 2), [[1, 2], [3, 4]])
        self.assertEqual(sudoku.group([1,2,3,4,5,6,7,8,9], 3), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_get_row(self):
        """get_row function test"""
        self.assertEqual(sudoku.get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0)), ['1', '2', '.'])
        self.assertEqual(sudoku.get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0)), ['4', '.', '6'])
        self.assertEqual(sudoku.get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0)), ['.', '8', '9'])
    
    def test_get_col(self):
        """get_col function test"""
        self.assertEqual(sudoku.get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0)), ['1', '4', '7'])
        self.assertEqual(sudoku.get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1)), ['2', '.', '8'])
        self.assertEqual(sudoku.get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2)), ['3', '6', '9'])

    def test_get_block(self):
        """get_block function test"""
        grid = sudoku.create_grid('53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        self.assertEqual(sudoku.get_block(grid, (0, 1)), ['5', '3', '.', '6', '.', '.', '.', '9', '8'])
        self.assertEqual(sudoku.get_block(grid, (4, 7)), ['.', '.', '3', '.', '.', '1', '.', '.', '6'])
        self.assertEqual(sudoku.get_block(grid, (8, 8)), ['2', '8', '.', '.', '.', '5', '.', '7', '9'])