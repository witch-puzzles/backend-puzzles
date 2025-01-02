import numpy
import typing
import random


class SudokuGrid:
    array: numpy.ndarray
    candidates: numpy.ndarray
    block_size: int
    grid_size: int

    """
    Contains functions to manipulate a Sudoku grid.
    A cell's value is either zero (which means it is empty), or between
    1-self.grid_size.

    grid_size = block_size * block_size
    """

    def __init__(self, block_size=3) -> typing.Self:
        """
        Generate an empty grid.
        """

        self.block_size = block_size
        self.grid_size = self.block_size * self.block_size
        self.array = numpy.zeros((self.grid_size, self.grid_size), dtype='uint8')
        self.candidates = numpy.zeros((self.grid_size, self.grid_size, self.grid_size), dtype='bool')

    # -- Static methods --
    @staticmethod
    def generate_filled(block_size: int = 3) -> typing.Self:
        """
        Generate a filled valid grid.
        Can be used to generate shuffled grids or test functions.
        """

        grid_size = block_size * block_size

        numbers = list(range(grid_size))
        random.shuffle(numbers)

        grid = SudokuGrid(block_size)
        for row_no in range(grid_size):
            for col_no in range(grid_size):
                grid.array[row_no, col_no] = numbers[(block_size * row_no + row_no // block_size + col_no) % grid_size] + 1

        return grid

    @staticmethod
    def generate_non_unique_puzzle(
            block_size: int = 3,
            empty: int = 40) -> typing.Self:

        """
        Generate an unsolved grid that may or may not have a unique solution.

        EMPTY determines how many empty squares should the grid have.
        """

        grid = SudokuGrid.generate_filled(block_size)

        # Select the first EMPTY items of the random squares list and clear the
        # squares.
        for square in SudokuGrid.generate_shuffled_squares(block_size)[:empty]:
            grid.array[square] = 0

        return grid

    @staticmethod
    def generate_unique_puzzle(
            block_size: int = 3,
            max_empty: int = -1) -> typing.Self:

        """
        Generate an unsolved grid that has a single unique solution.

        MAX_EMPTY determines how many empty squares the grid will have at most.
        This argument can be used to make sure than the algorithm does not take
        ages to generate a board. Using -1 will cause the generate to generate
        as much empty cells as possible.
        """

        grid = SudokuGrid.generate_filled(block_size)

        squares = SudokuGrid.generate_shuffled_squares(block_size)

        for square in squares:
            if max_empty == 0:
                break

            old_value = grid.array[square]

            # Remove a square and check if the puzzle still has a unique
            # solution.
            grid.array[square] = 0
            grid.generate_candidates()
            solutions = grid.try_solve_ms()

            # If there are no solutions, we know something went terribly wrong.
            assert solutions != 0, 'no solutions found?'

            if solutions == 2:
                grid.array[square] = old_value
            else:
                max_empty -= 1

        grid.generate_candidates()

        return grid

    @staticmethod
    def generate_squares(block_size: int = 3) -> [(int, int)]:
        """
        Generate a list of squares in increasing order.
        """

        grid_size = block_size * block_size
        return ((row_no, col_no) for row_no in range(grid_size) for col_no in range(grid_size))

    @staticmethod
    def generate_shuffled_squares(block_size: int = 3) -> [(int, int)]:
        """
        Generate a list of squares in random order.
        """

        squares = list(SudokuGrid.generate_squares(block_size))
        random.shuffle(squares)
        return squares

    @staticmethod
    def from_linear_notation(linear: str) -> typing.Self:
        """
        Generate a Grid object from a linear notation string
        """

        block_size, linear = linear.split(":", 1)
        block_size = int(block_size)
        grid_size = block_size * block_size
        linear = linear.split(",")

        grid = SudokuGrid(int(block_size))

        for row_no in range(grid.grid_size):
            for col_no in range(grid.grid_size):
                grid.array[row_no, col_no] = int(linear[row_no * grid_size + col_no])

        return grid

    @staticmethod
    def get_adjacent_squares(
            square: (int, int),
            block_size: int) -> typing.Generator[tuple[int, int], None, None]:

        """
        Return the list of adjacent squares.
        """

        grid_size = block_size * block_size
        row_no, col_no = square

        # Check for the values in the row.
        for new_col_no in range(grid_size):
            yield row_no, new_col_no

        # Check for the values in the column.
        for new_row_no in range(grid_size):
            yield new_row_no, col_no

        # Check for the values in the block.
        for new_row_no in range(row_no // block_size * block_size,
                                row_no // block_size * block_size + block_size):
            for new_col_no in range(col_no // block_size * block_size,
                                    col_no // block_size * block_size + block_size):
                yield new_row_no, new_col_no

    # -- ~*~Magic~*~ methods --
    def __repr__(self) -> str:
        characters = ' 123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        result = '+' + ('-' * self.block_size + '+') * self.block_size

        for row_block_no in range(self.block_size):
            result += '\n'
            for row_no in range(row_block_no * self.block_size,
                                row_block_no * self.block_size + self.block_size):
                result += '|'
                for col_block_no in range(self.block_size):
                    for col_no in range(col_block_no * self.block_size,
                                        col_block_no * self.block_size + self.block_size):
                        result += characters[self.array[row_no, col_no]]

                    result += '|'
                result += '\n'

            result += '+' + ('-' * self.block_size + '+') * self.block_size

        return result

    # -- Private methods --
    def _swap_rows(self, a: int, b: int) -> None:
        """
        Swaps two rows of the grid.
        This operation does not change the validness or the solvedness of the
        current grid if the rows are in the same row block.
        """

        self.array[[a, b], :] = self.array[[b, a], :]
        self.candidates[[a, b], :] = self.candidates[[b, a], :]

    def _swap_cols(self, a: int, b: int) -> None:
        """
        Swaps two columns of the grid.
        This operation does not change the validness or the solvedness of the
        current grid if the rows are in the same row block.
        """

        self.array[:, [a, b]] = self.array[:, [b, a]]
        self.candidates[:, [a, b]] = self.candidates[:, [b, a]]

    def _is_available(self, square: (int, int), number: int) -> bool:
        """
        Checks if a square can be set to a number.
        Checks for immediate consequences by looking for the same numbers in
        the row, column and the block.

        NOTE: The square should be empty.
        """

        # Check for all of the adjacent cells.
        for adjacent in SudokuGrid.get_adjacent_squares(square, self.block_size):
            if self.array[adjacent] == number:
                return False

        return True

    def _get_available(self, square: (int, int)) -> set[int]:
        """
        Returns the set of all available values for a square.
        Checks for the immediate consequences.

        NOTE: The square should be empty.
        """

        available = {i + 1 for i in range(self.grid_size) if self._is_available(square, i + 1)}

        return available

    def _update_candidates(self, square: typing.Tuple[int, int]) -> int:
        """
        Updates the candidates table after a square has been altered.
        """

        value = self.array[square]

        assert value > 0, "square should contain something"

        for adjacent in SudokuGrid.get_adjacent_squares(square, self.block_size):
            if self.array[adjacent] != 0:
                continue

            self.candidates[*adjacent, value - 1] = False

    # -- Public methods --
    def copy(self) -> typing.Self:
        """
        Generates a full copy of the grid object.
        """

        obj = SudokuGrid(self.block_size)
        obj.array = self.array.copy()
        obj.candidates = self.candidates.copy()
        return obj

    def shuffle(self) -> None:
        """
        Shuffles the rows and columns of the grid to generate a (almost) random
        board.
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

    def is_solved(self, only_valid=False) -> bool:
        """
        Checks if the grid is solved, aka if every cells has a number and the
        arrangement of the numbers does not break the regular Sudoku rules.
        If ONLY_VALID is True, does not check for the empty squares.
        """

        # Check for the rows.
        for row_no in range(self.grid_size):
            seen = set()
            for col_no in range(self.grid_size):
                number = self.array[row_no][col_no]

                if (not only_valid and number == 0) or number in seen:
                    return False

                if number != 0:
                    seen.add(number)

        # Check for the columns.
        for col_no in range(self.grid_size):
            seen = set()
            for row_no in range(self.grid_size):
                number = self.array[row_no][col_no]

                if (not only_valid and number == 0) or number in seen:
                    return False

                if number != 0:
                    seen.add(number)

        # Check for the blocks.
        for row_block_no in range(self.block_size):
            for col_block_no in range(self.block_size):
                seen = set()
                for row_no in range(row_block_no * self.block_size, row_block_no * self.block_size + self.block_size):
                    for col_no in range(col_block_no * self.block_size, col_block_no * self.block_size + self.block_size):
                        number = self.array[row_no][col_no]

                        if (not only_valid and number == 0) or number in seen:
                            return False

                        if number != 0:
                            seen.add(number)

        # All checks succeeded, return True.
        return True

    def generate_empty_cells(self) -> typing.Generator[tuple[int, int], None, None]:
        """
        Returns the list of empty cells on the board.
        """

        return ((row_no, col_no)
                for row_no in range(self.grid_size)
                for col_no in range(self.grid_size)
                if self.array[row_no, col_no] == 0)

    def generate_non_empty_cells(self) -> typing.Generator[tuple[int, int], None, None]:
        """
        Returns the list of non empty cells on the board.
        """

        return ((row_no, col_no)
                for row_no in range(self.grid_size)
                for col_no in range(self.grid_size)
                if self.array[row_no, col_no] != 0)

    def get_lowest_entropy_squares(self) -> tuple[int, set[tuple[int, int]]]:
        """
        Generates the list of squares that has the lowest amount of entropy.
        """

        lowest_entropy = self.grid_size
        lowest_entropy_squares = set()

        # Find the lowest entropy squares.
        for square in self.generate_empty_cells():
            available = self._get_available(square)

            if len(available) > lowest_entropy:
                continue

            if len(available) < lowest_entropy:
                lowest_entropy = len(available)
                lowest_entropy_squares.clear()

            lowest_entropy_squares.add(square)

        return lowest_entropy, lowest_entropy_squares

    def generate_candidates(self) -> numpy.ndarray:
        """
        Generates the candidates array.
        """

        self.candidates = numpy.zeros((self.grid_size, self.grid_size, self.grid_size), dtype='bool')

        for square in self.generate_empty_cells():
            if self.array[square] != 0:
                continue

            for avail in self._get_available(square):
                self.candidates[*square, avail - 1] = True

    def try_solve(self) -> None | typing.Self:
        """
        Tries to solve a grid using backtracking.
        If the grid is not completely filled and can not be solved, will
        return None and will try to solve some of the grid.
        If the grid is not completely filled and can be solved, will return
        the solution.

        NOTE: If the grid is completely filled but not solved, will still
              return a half solution.
        """

        copy = self.copy()

        if copy.solve_all_single_candidate() < 0:
            return None

        _, lowest_entropy_squares = copy.get_lowest_entropy_squares()
        if not lowest_entropy_squares:
            return copy

        square = lowest_entropy_squares.pop()

        for available in copy._get_available(square):
            candidates_copy = copy.candidates.copy()
            copy.array[square] = available
            copy._update_candidates(square)

            solution = copy.try_solve()

            if solution is not None:
                return solution

            copy.array[square] = 0
            copy.candidates = candidates_copy

        return None

    def try_solve_ms(self) -> int:
        """
        Tries to solve a grid using backtracking.
        Will not alter the grid.
        If the grid is not completely filled and can not be solved, will
        return 0.
        If the grid is not completely filled and has exactly one solution,
        will return 1.
        If the grid is not completely filled and more than one solutions, will
        return 2.

        NOTE: If the grid is completely filled, will return 1 no matter the
              number of solutions.
        """

        copy = self.copy()

        if copy.solve_all_single_candidate() < 0:
            return 0

        _, lowest_entropy_squares = copy.get_lowest_entropy_squares()
        if not lowest_entropy_squares:
            return True

        square = lowest_entropy_squares.pop()
        found_one_solution = False

        for available in copy._get_available(square):
            candidates_copy = copy.candidates.copy()
            copy.array[square] = available
            copy._update_candidates(square)

            solutions = copy.try_solve_ms()

            copy.array[square] = 0
            copy.candidates = candidates_copy

            if solutions == 1 and found_one_solution or solutions == 2:
                return 2

            if solutions == 1:
                found_one_solution = True

        return 1 if found_one_solution else 0

    def try_solve_classify(self, solution: numpy.ndarray) -> int:
        """
        Tries to solve and classify a grid.
        Returns the difficulty level of a grid.
        The difficulty is calculated by counting the number of required
        assumptions on average to solve.
        """

        copy = self.copy()

        # Try to solve all of the single candidate solutions, if there are no
        # possible solutions return immediately.
        if copy.solve_all_single_candidate() < 0:
            return -1

        lowest_entropy, lowest_entropy_squares = copy.get_lowest_entropy_squares()

        if not lowest_entropy_squares:
            return 0

        # After a call to solve_all_single_candidate, the lowest entropy can not be 0 or 1.
        assert lowest_entropy >= 2

        # Start making assumptions on one of the lowest entropy squares.
        square = random.choice(list(lowest_entropy_squares))
        copy_copy = copy.copy()

        copy_copy.array[square] = solution[square]
        copy_copy._update_candidates(square)

        next_iteration = copy_copy.try_solve_classify(solution)

        if next_iteration >= 0:
            return next_iteration + 1

        # None of the available digits solved the puzzle, therefore the puzzle is unsolvable.
        return -1

    def solve_all_single_candidate(self) -> int:
        """
        Solve all of the single candidate squares.
        Returns -1 if the grid is unsolvable.
        Returns >=0 if the grid MAY BE solvable, the number of solved squares.
        """

        squares = set(SudokuGrid.generate_squares(self.block_size))
        total = 0

        while squares:
            square = squares.pop()

            if self.array[square] != 0:
                continue

            available = self._get_available(square)

            if not len(available):
                return -1

            if len(available) == 1:
                self.array[square] = available.pop()
                self._update_candidates(square)
                total += 1
                squares.update(SudokuGrid.get_adjacent_squares(square, self.block_size))

        return total

    @property
    def linear_notation(self) -> str:
        """
        Returns the linear notation for the sudoku board.
        """

        result = f'{self.block_size}:'

        for row_no in range(self.grid_size):
            for col_no in range(self.grid_size):
                result += f'{self.array[row_no, col_no]},'

        return result[:-1]
