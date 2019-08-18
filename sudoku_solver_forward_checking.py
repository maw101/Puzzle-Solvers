from copy import deepcopy as dc


def render_grid(grid):
    if grid is None:
        print("No Solution")
    else:
        # print each row and values in grid
        for row in range(9):
            row_string = ""
            for col in range(9):
                row_string += str(grid[col][row]) + " "
                if col in [2, 5]:  # print divider every 3 columns
                    row_string += "| "
            print(row_string)
            if row in [2, 5]:  # print divider every 3 rows
                print("---------------------")

def render_grid_with_sets(grid):  # used for debug purposes
    if grid is not None:
        # print each row and values in grid
        for row in range(9):
            row_string = ""
            for col in range(9):
                row_string += str(grid[col][row]) + ","
                if col in [2, 5]:  # print divider every 3 columns
                    row_string += "| "
            print(row_string)
            if row in [2, 5]:  # print divider every 3 rows
                print("---------------------")


def forwardCheck(grid):
    grid_changed = False

    # go through each x position in grid - ie each column
    for x in range(9):
        # get all positions in current column
        column = grid[x]
        # get all values that are set in stone within the column
        #   only adds values to the set if they are not an instance of a set
        #   ie when there is only one value in the position
        final_values_in_column = set([val for val in column if not isinstance(val, set)])
        # loop through each row in the column
        for y in range(9):
            # check if current position refers to set - if it does then value not set yet and we are still finding it
            if isinstance(grid[x][y], set):
                # try to set value
                # get set difference between position and values already set in the column
                grid[x][y] = grid[x][y] - final_values_in_column
                if len(grid[x][y]) == 1:  # can set this single value in stone
                    # get the only value from the positions set and store it in the position
                    grid[x][y] = grid[x][y].pop()
                    final_values_in_column.add(grid[x][y])  # add to the set of 'set in stone'/final values
                    grid_changed = True
                elif len(grid[x][y]) == 0:  # shouldn't have happened
                    return False, None

    # go through each y position in grid - ie each row
    for y in range(9):
        # get all positions in current row
        row = [grid[x][y] for x in range(9)]

        # get all values that are set in stone within the row
        #   only adds values to the set if they are not an instance of a set
        #   ie when there is only one value in the position
        final_values_in_row = set([val for val in row if not isinstance(val, set)])
        # loop through each column in the row
        for x in range(9):
            # check if current position refers to set - if it does then value not set yet and we are still finding it
            if isinstance(grid[x][y], set):
                # try to set value
                # get set difference between position and values already set in the column
                grid[x][y] = grid[x][y] - final_values_in_row
                if len(grid[x][y]) == 1:  # can set this single value in stone
                    # get the only value from the positions set and store it in the position
                    grid[x][y] = grid[x][y].pop()
                    final_values_in_row.add(grid[x][y])  # add to the set of 'set in stone'/final values
                    grid_changed = True
                elif len(grid[x][y]) == 0:  # shouldn't have happened
                    return False, None

    # go through each cell in each square in grid
    for square_x in [0, 3, 6]:
        for square_y in [0, 3, 6]:
            # get all values that are 'set in stone'/final within the 3x3 square
            #   we will add such values to this set. Final values will not be an
            #   instance of a set when checking a position.
            final_values_in_square = set()
            # check all positions in square for possible final values - ie positions not an instance of a set
            for x in range(square_x, square_x + 3):
                for y in range(square_y, square_y + 3):
                    if not isinstance(grid[x][y], set):
                        final_values_in_square.add(grid[x][y])  # add to the set of final values
            # loop through each position in the square
            for x in range(square_x, square_x + 3):
                for y in range(square_y, square_y + 3):
                    # check if current position refers to set - if it does then value not set yet, still finding it
                    if isinstance(grid[x][y], set):
                        # try to set value
                        # get set difference between position and values already set in the column
                        grid[x][y] = grid[x][y] - final_values_in_square
                        if len(grid[x][y]) == 1:  # can set this single value in stone
                            # get the only value from the positions set and store it in the position
                            grid[x][y] = grid[x][y].pop()
                            final_values_in_square.add(grid[x][y])  # add to the set of 'set in stone'/final values
                            grid_changed = True
                        elif len(grid[x][y]) == 0:  # shouldn't have happened
                            return False, None

    return True, grid_changed


def getValidCompleteGrid(grid):
    # loop until the grid has not been changed OR if we determine that the grid cannot be solved
    while True:
        can_be_solved, grid_changed = forwardCheck(grid)
        if not can_be_solved:  # grid cannot be solved - terminate
            return False
        elif not grid_changed:  # grid cannot be processed any more
            return True


def solve(grid):
    resolveZerosInGrid(grid)

    can_be_solved = getValidCompleteGrid(grid)
    if not can_be_solved:
        return None
    elif checkIfSolveCompleted(grid):
        return grid

    # we must still have positions containing sets - try each of the values in the set
    # go through each y position in grid - ie each row
    for y in range(9):
        # loop through each column in the row
        for x in range(9):
            # check if current position refers to set
            if isinstance(grid[x][y], set):
                for val in grid[x][y]:  # go through each value in the set
                    new_grid = dc(grid)  # perform deep copy of the grid as we will be altering values
                    new_grid[x][y] = val  # try the current value in the set as the final value and propogate
                    can_be_solved = solve(new_grid)  # check if the newly assigned value leads to a solved grid
                    if can_be_solved is not None:  # has been solved - return solved grid
                        return can_be_solved
                return None  # no value in the set caused the solve to complete


def checkIfSolveCompleted(grid):
    for y in range(9):
        for x in range(9):
            # check if position is instance of a set
            #   if it is then it means the value has not been made final and so the solve isn't complete
            if isinstance(grid[x][y], set):
                return False
    return True

def resolveZerosInGrid(grid):
    for y in range(9):
        for x in range(9):
            if grid[x][y] == 0:  # replace with set of possible values
                grid[x][y] = set(range(1, 10))