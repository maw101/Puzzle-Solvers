# PuzzleSolvers

## Sudoku Solver
A Sudoku Solving Algorithm which utilises Constraint Propagation in order to more efficiently determine the solution to a Sudoku puzzle.

Forward Checking is implemented which prevents future conflicts. This is achieved by storing a set of possible values for a position which does not have a final value. This is propogated for the rest of the Sudoku and so the possible values for a position are greatly reduced. This means that we only try valid values and discount those already set in the row, column and square. 

### Solving Validation
Utilising several datasets found at [http://magictour.free.fr/sudoku.htm](http://magictour.free.fr/sudoku.htm).

| Dataset | # Puzzles | # Solved | Average Solve Time (s) | Maximum Solve Time (s) |
|---------|-----------|----------|------------------------|------------------------|
|[top95](http://magictour.free.fr/top95)|95|95|0.7366267738526316|9.169138592|
|[topn87](http://magictour.free.fr/topn87)|87|87|0.5242678814942529|5.606698960999999|
|[topn234](http://magictour.free.fr/topn234)|234|234|0.7892137054102566|21.929735709|
|[top1465](http://magictour.free.fr/top1465)|1465|1465|0.25345617703344697|21.777229609000003|
