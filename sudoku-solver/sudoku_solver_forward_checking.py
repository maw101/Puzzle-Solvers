import logging
logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(levelname)s %(message)s")

import time

####################################################################################################
class Grid:
    ################################################################################################
    def __init__(self, size=9):
        if size % 3 != 0:
            raise ValueError("Grid size must be a multiple of 3.")
        self.size = size
        self.grid = self.__get_blank_grid()

    ################################################################################################
    def is_filled(self):
        for y in range(self.size):
            for x in range(self.size):
                # check if position is instance of a set - if it is then it means the value has not
                #   been made final and so the solve isn't complete
                if isinstance(self.grid[x][y], set) and len(self.grid[x][y]) > 1:
                    return False
        return True

    ################################################################################################
    def deep_copy(self):
        grid_copy = self.__get_blank_grid()
        for y in range(self.size):
            for x in range(self.size):
                grid_copy[x][y] = self.grid[x][y]

        self.__resolve_zeros_in_grid(grid_copy)

        return grid_copy

    ################################################################################################
    def parse_string(self, grid_as_string):
        if len(grid_as_string) != (self.size ** 2):
            raise RuntimeError(
                "String representation invalid, incorrect number of characters for a {}x{} Sudoku.".format(self.size, self.size))

        for y in range(self.size):
            for x in range(self.size):
                val = grid_as_string[x + (self.size * y)]
                if val == '.':
                    self.grid[x][y] = set(range(1, (self.size + 1)))
                else:
                    self.grid[x][y] = val
        
        return self

    ################################################################################################
    def __resolve_zeros_in_grid(self, grid):
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[x][y] == 0:  # replace with set of possible values
                    self.grid[x][y] = set(range(1, (self.size + 1)))

    ################################################################################################
    def __get_blank_grid(self):
        return [[0 for x in range(self.size)] for y in range(self.size)]

####################################################################################################
class RenderCLI:
    ################################################################################################
    @staticmethod
    def render_grid(grid):
        if (not grid) or (not grid.grid):
            print("No Solution")
        else:
            square_size = grid.size // 3
            # NOTE: +2 at end to allow for the two vertical dividers, -1 to account for extra space at end
            horizontal_divider = '-' * ((2 * (grid.size + 2)) - 1)

            # print formatted grid
            for row in range(grid.size):
                row_string = ""
                for col in range(grid.size):
                    row_string += "{} ".format(grid.grid[col][row])
                    # print divider to separate squares
                    if ((col + 1) % square_size == 0) and (col != (grid.size - 1)):
                        row_string += "| "

                print(row_string)

                # print divider to separate squares
                if ((row + 1) % square_size == 0) and (row != (grid.size - 1)):
                    print(horizontal_divider)

            if grid.is_filled():
                print() # NOTE: blank line
                print("Grid is filled.")


####################################################################################################
class SudokuSolver():
    ################################################################################################
    def solve(self, grid):
        if grid.size != 9:
            raise NotImplementedError(
                "Sudoku solver only supports 9x9 Sudoku's at this time.")

        can_be_solved = self.__get_valid_complete_grid(grid)
        if not can_be_solved:
            return None
        if grid.is_filled():
            return grid

        # Grid not filled, we must still have positions containing sets - try each of these values
        for y in range(grid.size):  # rows
            for x in range(grid.size):  # columns
                # check if current position refers to set
                if isinstance(grid.grid[x][y], set):
                    for val in grid.grid[x][y]:
                        # Try the current value from the set as the final value for the position,
                        #   and propagate
                        new_grid = Grid()
                        new_grid.grid = grid.deep_copy()
                        new_grid.grid[x][y] = val

                        # check if the newly assigned value leads to a solved grid
                        solved = self.solve(new_grid)
                        if solved:
                            return solved

                    return None  # no value in the set worked for the current position

    ################################################################################################
    def __get_valid_complete_grid(self, grid):
        # loop until the grid has not been changed OR if we determine that the grid cannot be solved
        while True:
            can_be_solved, grid_changed = self.__forward_check(grid)
            if not can_be_solved:  # grid cannot be solved - terminate
                return False
            if not grid_changed:  # grid cannot be processed any more
                return True

    ################################################################################################
    def __forward_check(self, grid):
        ############################################################################################
        def process_position(x, y, final_values):
            # check if we are still determining a value for the current position (set instance)
            if isinstance(grid.grid[x][y], set):
                # try to set value
                # get set difference between position and values already set
                grid.grid[x][y] = grid.grid[x][y] - final_values

                # can set this single value in stone
                if len(grid.grid[x][y]) == 1:
                    # get the only value from the positions set and store it in the position
                    grid.grid[x][y] = grid.grid[x][y].pop()
                    # add to the set of 'set in stone'/final values
                    final_values.add(int(grid.grid[x][y]))
                    return True # grid changed
                elif len(grid.grid[x][y]) == 0: # shouldn't have 0 possibilities, error occurred
                    return None # grid unable to be changed

            return False # grid not changed

        grid_changed = False

        for x in range(grid.size):  # columns
            column = grid.grid[x]  # get all positions
            # get all values that are set in stone within the column
            #   only adds values to the set if they are not an instance of a set
            #   i.e. when there is only one value in the position
            final_values_in_column = set(
                [int(val) for val in column if not isinstance(val, set)])

            for y in range(grid.size):  # rows
                result = process_position(x, y, final_values_in_column)
                if result is None:
                    return False, None
                grid_changed = result

        for y in range(grid.size):  # rows
            row = [grid.grid[x][y]
                   for x in range(grid.size)]  # get all positions

            # get all values that are set in stone within the row
            #   only adds values to the set if they are not an instance of a set
            #   i.e. when there is only one value in the position
            final_values_in_row = set(
                [int(val) for val in row if not isinstance(val, set)])

            for x in range(grid.size):  # columns
                result = process_position(x, y, final_values_in_row)
                if result is None:
                    return False, None
                grid_changed = result

        # check each squares cells
        square_size = grid.size // 3
        
        for square_x in [0, square_size, (2 * square_size)]:
            for square_y in [0, square_size, (2 * square_size)]:
                # get all values that are 'set in stone'/final within the 3x3 square
                #   we will add such values to this set. Final values will not be an
                #   instance of a set when checking a position.
                final_values_in_square = set()
                # check all positions in square for possible final values - i.e. not a set instance
                for x in range(square_x, square_x + square_size):
                    for y in range(square_y, square_y + square_size):
                        if not isinstance(grid.grid[x][y], set):
                            # add to the set of final values
                            final_values_in_square.add(int(grid.grid[x][y]))

                # loop through each position in the square
                for x in range(square_x, square_x + square_size):
                    for y in range(square_y, square_y + square_size):
                        result = process_position(x, y, final_values_in_square)
                        if result is None:
                            return False, None
                        grid_changed = result

        return True, grid_changed


####################################################################################################
class BenchmarkSolver:
    ################################################################################################
    def solve_file(self, filename):
        all_grids_as_str = self.__parse_file(filename)
        logging.info("{} grid(s) to solve".format(len(all_grids_as_str)))

        # process all grids in turn
        g = Grid()
        times, solved = zip(*[self.__timed_solve(g.parse_string(g_as_str))
                            for g_as_str in all_grids_as_str])
        
        grid_count = len(all_grids_as_str)
        self.__print_stats(times, solved, grid_count)

    ################################################################################################
    def __parse_file(self, filename):
        f = open(filename, "r")
        return f.read().strip().split("\n")

    ################################################################################################
    def __timed_solve(self, grid):
        solver = SudokuSolver()

        start_time = time.process_time()
        processed_grid = solver.solve(grid)
        time_to_solve = time.process_time() - start_time

        solved = processed_grid.is_filled()
        if solved:
            logging.info("Grid solved in {} seconds".format(time_to_solve))

        return time_to_solve, solved

    ################################################################################################
    def __print_stats(self, times, solved, grid_count):
        if grid_count:
            puzzles_solved = len(solved)
            average_per_grid = sum(times) / grid_count
            longest_solve_time = max(times)
            logging.info("{} puzzles solved (out of {}) in an average of {} second(s). Longest time to solve was {} second(s).".format(
                puzzles_solved, grid_count, average_per_grid, longest_solve_time))


####################################################################################################
if __name__ == "__main__":
    grid = Grid()
    grid.parse_string("8....53......8......24.76........4.33......96..97.41.........321.....7..67.......")

    s = SudokuSolver()
    grid = s.solve(grid)

    RenderCLI().render_grid(grid)

    # Benchmarks
    benchmarker = BenchmarkSolver()
    benchmarker.solve_file("Sudoku-Grids/top1465.txt")
