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

    def test_find_empty_positions(self):
        """find_empty_positions function test"""
        self.assertEqual(sudoku.find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]), (0, 2))
        self.assertEqual(sudoku.find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']]), (1, 1))
        self.assertEqual(sudoku.find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']]), (2, 0))

    def test_find_possible_values(self):
        """find_possible_values function test"""
        grid = sudoku.create_grid('53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        self.assertEqual(sudoku.find_possible_values(grid, (0,2)), {'1', '2', '4'})
        self.assertEqual(sudoku.find_possible_values(grid, (4,7)), {'2', '5', '9'})
    
    def test_solve(self):
        """solve function test"""
        grid = sudoku.create_grid('53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        self.assertEqual(sudoku.solve(grid), [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']])

    def test_generate_sudoku(self):
        """generate_sudoku function test"""
        grid = sudoku.generate_sudoku(40)
        self.assertEqual(sum(1 for row in grid for e in row if e == '.'), 41)

        solution = sudoku.solve(grid)
        self.assertEqual(sudoku.check_solution(solution), True)

        grid = sudoku.generate_sudoku(1000)
        self.assertEqual(sum(1 for row in grid for e in row if e == '.'), 0)

        solution = sudoku.solve(grid)
        self.assertEqual(sudoku.check_solution(solution), True)

        grid = sudoku.generate_sudoku(0)
        self.assertEqual(sum(1 for row in grid for e in row if e == '.'), 81)

        solution = sudoku.solve(grid)
        self.assertEqual(sudoku.check_solution(solution), True)
        