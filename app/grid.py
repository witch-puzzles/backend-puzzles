import numpy
import typing
import random


class Grid:
    array: numpy.ndarray

    """
    Contains functions to manipulate a Sudoku grid.
    A cells value is either zero (which means it is empty), or between 1-self.grid_size.
    """

    def __init__(self) -> typing.Self:
        """
        Generate an empty grid.
        """

        self.block_size = 3
        self.grid_size = self.block_size * self.block_size
        self.array = numpy.zeros((self.grid_size, self.grid_size), dtype='int8')

    # -- Static methods --
    @staticmethod
    def generate_simple(block_size: int) -> typing.Self:
        """
        Generate a simple solved grid.
        Can be used to generate shuffled grids or test functions.
        """

        grid_size = block_size * block_size

        numbers = list(range(grid_size))
        random.shuffle(numbers)

        grid = Grid()
        for row_no in range(grid_size):
            for col_no in range(grid_size):
                grid.array[row_no, col_no] = numbers[(block_size * row_no + row_no // block_size + col_no) % grid_size] + 1

        return grid

    # -- ~Magic~ methods --
    def __repr__(self) -> str:
        characters = ' 123456789ABCDEFG'

        result = '+' + ('-' * self.block_size + '+') * self.block_size

        for row_block_no in range(self.block_size):
            result += '\n'
            for row_no in range(row_block_no * self.block_size, row_block_no * self.block_size + self.block_size):
                result += '|'
                for col_block_no in range(self.block_size):
                    for col_no in range(col_block_no * self.block_size, col_block_no * self.block_size + self.block_size):
                        result += characters[self.array[row_no, col_no]]

                    result += '|'
                result += '\n'

            result += '+' + ('-' * self.block_size + '+') * self.block_size

        return result

    # -- Private methods --
    def _swap_rows(self, a: int, b: int) -> None:
        """
        Swaps two rows of the grid.
        """

        self.array[[a, b], :] = self.array[[b, a], :]

    def _swap_cols(self, a: int, b: int) -> None:
        """
        Swaps two columns of the grid.
        """

        self.array[:, [a, b]] = self.array[:, [b, a]]

    def _is_available(self, square: (int, int), number: int) -> bool:
        """
        Checks if a square can be set to a number.
        Checks for immediate consequences by looking for the same numbers in the row, column and the block.

        NOTE: The square should be empty.
        """

        row_no, col_no = square

        # Check for the values in the row.
        for new_col_no in range(self.grid_size):
            if self.array[row_no][new_col_no] == number:
                return False

        # Check for the values in the column.
        for new_row_no in range(self.grid_size):
            if self.array[new_row_no][col_no] == number:
                return False

        # Check for the values in the block.
        for new_row_no in range(row_no // self.block_size * self.block_size, row_no // self.block_size * self.block_size + self.block_size):
            for new_col_no in range(col_no // self.block_size * self.block_size, col_no // self.block_size * self.block_size + self.block_size):
                if self.array[new_row_no][new_col_no] == number:
                    return False

        # All checks succeded.
        return True


    def _try_solve_square(self, i: int, squares: list) -> bool:
        """
        Tries to solve a grid using backtracking.
        Should be called from the solve method.
        """

        square = squares[i]

        for number in range(1, self.grid_size + 1):
            if not self._is_available(square, number):
                continue

            self.array[square] = number

            if i == len(squares) - 1:
                return True

            if self._try_solve_square(i + 1, squares):
                return True

            self.array[square] = 0

        return False

    # -- Public methods --
    def copy(self) -> typing.Self:
        """
        Generates a full copy of the grid object.
        """

        obj = Grid()
        obj.array = self.array.copy()
        return obj

    def shuffle(self) -> None:
        """
        Shuffles the rows and columns of the grid to generate a (almost) random board.
        """

        # Shuffle the rows inside blocks.
        for row_block_no in range(self.block_size):
            for row_no in range(row_block_no * self.block_size, row_block_no * self.block_size + self.block_size):
                chosen_one = random.randrange(row_block_no * self.block_size, row_block_no * self.block_size + self.block_size)
                self._swap_rows(row_no, chosen_one)

        # Shuffle the columns inside blocks.
        for col_block_no in range(self.block_size):
            for col_no in range(col_block_no * self.block_size, col_block_no * self.block_size + self.block_size):
                chosen_one = random.randrange(col_block_no * self.block_size, col_block_no * self.block_size + self.block_size)
                self._swap_cols(col_no, chosen_one)

        # Shuffle the row blocks.
        for row_block_no in range(self.block_size):
            chosen_one = random.randrange(0, self.block_size)
            for i in range(self.block_size):
                row_no = row_block_no * self.block_size + i
                new_row_no = chosen_one * self.block_size + i
                self._swap_rows(row_no, new_row_no)

        # Shuffle the column blocks.
        for col_block_no in range(self.block_size):
            chosen_one = random.randrange(0, self.block_size)
            for i in range(self.block_size):
                col_no = col_block_no * self.block_size + i
                new_col_no = chosen_one * self.block_size + i
                self._swap_cols(col_no, new_col_no)

    def is_solved(self) -> None:
        """
        Checks if the grid is solved, aka if every cells has a number and the
        arrangement of the numbers does not break the regular Sudoku rules.
        """

        # Check for the rows.
        for row_no in range(self.grid_size):
            seen = set()
            for col_no in range(self.grid_size):
                number = self.array[row_no][col_no]

                if number == 0 or number in seen:
                    return False

                seen.add(number)

        # Check for the columns.
        for col_no in range(self.grid_size):
            seen = set()
            for row_no in range(self.grid_size):
                number = self.array[row_no][col_no]

                if number == 0 or number in seen:
                    return False

                seen.add(number)

        # Check for the blocks.
        for row_block_no in range(self.block_size):
            for col_block_no in range(self.block_size):
                seen = set()
                for row_no in range(row_block_no * self.block_size, row_block_no * self.block_size + self.block_size):
                    for col_no in range(col_block_no * self.block_size, col_block_no * self.block_size + self.block_size):
                        number = self.array[row_no][col_no]

                        if number == 0 or number in seen:
                            return False

                        seen.add(number)

        # All checks succeeded, return True.
        return True

    def try_solve(self) -> bool:
        """
        Tries to solve a grid.
        Returns if the grid is solvable.

        TODO: This function should also keep track of the available numbers for
              each square as this would improve the performance quite a lot.
        """

        # Get a list of empty squares.
        squares = [(row_no, col_no)
                   for row_no in range(self.grid_size)
                   for col_no in range(self.grid_size)
                   if self.array[row_no, col_no] == 0]

        self._try_solve_square(0, squares)


grid = Grid.generate_simple(3)
grid.shuffle()
print(grid)
print(grid.is_solved())
