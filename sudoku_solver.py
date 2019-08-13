class SudokuSolver:

    DIMENSION = 9
    grid = []

    def __init__(self, grid):
        self.grid = [[' ' for column in range(self.DIMENSION)] for row in range(self.DIMENSION)]

    def render_grid(self):
        # print each row and values in grid
        for row in range(self.DIMENSION):
            row_string = ""
            for col in range(self.DIMENSION):
                row_string += str(self.grid[col][row]) + " "
                if col in [2, 5]: # print divider every 3 columns
                    row_string += "| "
            print(row_string)
            if row in [2, 5]: # print divider every 3 rows
                print("---------------------")

s = SudokuSolver()
s.render_grid()
