import unittest
import numpy as np
from app.libs.sudoku_grid import SudokuGrid

class TestSudokuGrid(unittest.TestCase):

    def test_generate_filled(self):
        # Test the generate_filled method
        block_size = 3
        grid = SudokuGrid.generate_filled(block_size)

        # Check if the grid is filled with valid values
        self.assertEqual(grid.is_solved(only_valid=True), True)

    def test_generate_non_unique_puzzle(self):
        # Test the generate_non_unique_puzzle method
        block_size = 3
        empty = 40
        grid = SudokuGrid.generate_non_unique_puzzle(block_size, empty)

        # Ensure that the grid is not solved but is valid after generation
        self.assertEqual(grid.is_solved(), False)
        self.assertEqual(grid.is_solved(True), True)

    def test_generate_unique_puzzle(self):
        # Test the generate_unique_puzzle method
        block_size = 3
        grid = SudokuGrid.generate_unique_puzzle(block_size)

        # Ensure that the grid is not solved but is valid after generation
        self.assertEqual(grid.is_solved(), False)
        self.assertEqual(grid.is_solved(True), True)

    def test_generate_empty_cells(self):
        # Test generate_empty_cells method
        grid = SudokuGrid.generate_filled(3)
        grid.array[0, 0] = 0  # Make one cell empty

        empty_cells = list(grid.generate_empty_cells())

        self.assertEqual(len(empty_cells), 1)
        self.assertEqual(empty_cells[0], (0, 0))

    def test_generate_non_empty_cells(self):
        # Test generate_non_empty_cells method
        grid = SudokuGrid.generate_filled(3)
        grid.array[0, 0] = 0  # Make one cell empty

        non_empty_cells = list(grid.generate_non_empty_cells())

        self.assertEqual(len(non_empty_cells), grid.grid_size * grid.grid_size - 1)

    def test_is_solved(self):
        # Test is_solved method
        grid = SudokuGrid.generate_filled(3)
        self.assertEqual(grid.is_solved(), True)

        # Test with an unsolved grid
        grid.array[0, 0] = 0
        self.assertEqual(grid.is_solved(), False)

    def test_copy(self):
        # Test copy method
        grid = SudokuGrid.generate_filled(3)
        grid_copy = grid.copy()

        # Ensure the copied grid is identical but not the same object
        self.assertEqual(np.array_equal(grid.array, grid_copy.array), True)
        self.assertNotEqual(id(grid), id(grid_copy))

    def test_get_lowest_entropy_squares(self):
        # Test get_lowest_entropy_squares method
        grid = SudokuGrid.generate_filled(3)

        entropy, squares = grid.get_lowest_entropy_squares()

        self.assertEqual(entropy, 9)  # Maximum entropy since it's a filled grid
        self.assertEqual(len(squares), 0)  # No empty squares, hence no lowest entropy squares

    def test_generate_candidates(self):
        # Test generate_candidates method
        grid = SudokuGrid.generate_non_unique_puzzle(3)
        grid.generate_candidates()

        # Ensure that candidates are generated
        self.assertEqual(np.any(grid.candidates), True)

    def test_try_solve(self):
        # Test try_solve method
        grid = SudokuGrid.generate_unique_puzzle(3)
        solved_grid = grid.try_solve()

        # Check if the grid was solved
        self.assertIsNotNone(solved_grid)
        self.assertTrue(solved_grid.is_solved())

    def test_try_solve_ms(self):
        # Test try_solve_ms method
        grid = SudokuGrid.generate_unique_puzzle(3)
        result = grid.try_solve_ms()

        # Ensure that the puzzle has exactly one solution
        self.assertEqual(result, 1)

    def test_from_linear_notation(self):
        # Test from_linear_notation method
        linear_notation = "3:1,2,3,4,5,6,7,8,9,4,5,6,7,8,9,1,2,3,5,6,7,8,9,1,2,3,6,7,8,9,1,2,3,7,8,9,1,2,3,8,9,1,2,3,4,5,6,9,1,2,3,4,5,6,1,2,3,4,5,6,7,8,9,4,5,6,7,8,9,1,2,3,5,6,7,8,9,1,2,3,6,7,8,9,1,2,3"
        grid = SudokuGrid.from_linear_notation(linear_notation)

        # Ensure the grid is generated correctly from linear notation
        self.assertEqual(grid.array[0, 0], 1)
        self.assertEqual(grid.array[0, 1], 2)

    def test_is_available(self):
        # Test _is_available method
        grid = SudokuGrid.generate_filled(3)
        initial = grid.array[0, 0]
        grid.array[0, 0] = 0  # Make one cell empty
        grid.generate_candidates()

        # Check availability of number 5 in the empty cell (0, 0)
        is_available = grid._is_available((0, 0), initial)

        # Since it's an empty grid and the number is not used in the same row, column, or block
        self.assertTrue(is_available)


if __name__ == "__main__":
    unittest.main()
