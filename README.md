# PuzzleSolvers

## [Sudoku Solver](/sudoku-solver).

A Sudoku Solving Algorithm which utilises Constraint Propagation in order to more efficiently determine the solution to a Sudoku puzzle.

Forward Checking is implemented which prevents future conflicts. This is achieved by storing a set of possible values for a position which does not have a final value. This is propogated for the rest of the Sudoku and so the possible values for a position are greatly reduced. This means that we only try valid values and discount those already set in the row, column and square. 

### Solving Validation
Utilising several datasets found at [http://magictour.free.fr/sudoku.htm](http://magictour.free.fr/sudoku.htm).

| Dataset | # Puzzles | # Solved | Average Solve Time (s) | Maximum Solve Time (s) |
|---------|-----------|----------|------------------------|------------------------|
|[top95](Sudoku-Grids/top95.txt)|95|95|0.7366267738526316|9.169138592|
|[topn87](Sudoku-Grids/topn87.txt)|87|87|0.5242678814942529|5.606698960999999|
|[topn234](Sudoku-Grids/topn234.txt)|234|234|0.7892137054102566|21.929735709|
|[top1465](Sudoku-Grids/top1465.txt)|1465|1465|0.25345617703344697|21.777229609000003|


## [K-Puzzle Solver](/k-puzzle-solver).

A K-Puzzle Solving Algorithm which utliises a general AI methodology known as the [A* Search Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm).

Efficiently solves 8-puzzles (3x3 tiles) - a variation of a [15 puzzle](https://en.wikipedia.org/wiki/15_puzzle).

## License

[GNU General Public License v3.0](https://github.com/maw101/PuzzleSolvers/blob/master/LICENSE)
