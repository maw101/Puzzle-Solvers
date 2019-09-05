import java.util.Stack;

public class Board {

    private final int[] tiles;
    private final int n;

    // create a board from an n-by-n array of tiles,
    // where tiles[row][col] = tile at (row, col)
    public Board(int[][] tiles) {
        this.n = tiles.length;
        this.tiles = new int[n * n];
        // deep copy
        for (int row = 0; row < n; row++)
            for (int column = 0; column < n; column++)
                this.tiles[(row * n) + column] = tiles[row][column];
    }

    private Board(int[] tiles) {
        this.n = (int) Math.sqrt(tiles.length);
        this.tiles = new int[n * n];
        for (int i = 0; i < n * n; i++)
            this.tiles[i] = tiles[i];
    }

    // string representation of this board
    public String toString() {
        StringBuilder str = new StringBuilder();
        str.append(n + "\n");
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                str.append(" " + tiles[(i * n) + j]);
            }
            str.append("\n");
        }
        return str.toString();
    }

    public int dimension() {
        return this.n;
    }

    // number of tiles out of place
    public int hamming() {
        int todoCount = 0;
        for (int i = 0; i < n * n; i++)
            if (isTileOutOfPlace(i))
                todoCount++;
        return todoCount;
    }

    // sum of Manhattan distances between tiles and goal
    public int manhattan() {
        int sum = 0;
        for (int i = 0; i < n * n; i++)
            if (isTileOutOfPlace(i))
                sum += manhattan(i, tiles[i]);
        return sum;
    }

    private int manhattan(int currentValue, int goalValue) {
        int rowDiff, colDiff;
        rowDiff = Math.abs((goalValue - 1) / n - currentValue / n);
        colDiff = Math.abs((goalValue - 1) % n - currentValue % n);
        return rowDiff + colDiff;
    }

    private boolean isTileOutOfPlace(int index) {
        return (tiles[index] != (index + 1)) && (tiles[index] != 0);
    }

    // is this board the goal board?
    public boolean isGoal() {
        for (int i = 0; i < (n * n) - 1; i++)
            if (tiles[i] != (i + 1))
                return false;
        return true;
    }

    // does this board equal y?
    public boolean equals(Object y) {
        if (y == this)
            return true;
        if (y == null)
            return false;
        if (y.getClass() != this.getClass())
            return false;

        Board that = (Board) y;

        // check dimension
        if (this.n != that.n)
            return false;

        // check each tile in turn
        for (int i = 0; i < tiles.length; i++)
            if (this.tiles[i] != that.tiles[i])
                return false;

        return true;
    }

    // all neighboring boards
    public Iterable<Board> neighbors() {
        Stack<Board> neighbours = new Stack<>();
        int blankTileIndex = getBlankTileIndex();
        int blankTileI = blankTileIndex / n;
        int blankTileJ = blankTileIndex % n;

        if (blankTileI > 0)
            neighbours.push(new Board(swapTwoTiles(blankTileI, blankTileJ, (blankTileI - 1), blankTileJ)));
        if (blankTileI < (n - 1))
            neighbours.push(new Board(swapTwoTiles(blankTileI, blankTileJ, (blankTileI + 1), blankTileJ)));
        if (blankTileJ > 0)
            neighbours.push(new Board(swapTwoTiles(blankTileI, blankTileJ, blankTileI, (blankTileJ - 1))));
        if (blankTileJ < (n - 1))
            neighbours.push(new Board(swapTwoTiles(blankTileI, blankTileJ, blankTileI, (blankTileJ + 1))));

        return neighbours;
    }

    private int getBlankTileIndex() {
        for (int i = 0; i < tiles.length; i++)
            if (tiles[i] == 0)
                return i;
        throw new NoSuchFieldError("No Blank Tile present on the grid"); // error - no blank tile?
    }

    private int[] swapTwoTiles(int i, int j, int i2, int j2) {
        int[] copiedBoard = tiles.clone();
        int tempTileValue = copiedBoard[(i * n) + j];
        copiedBoard[(i * n) + j] = copiedBoard[(i2 * n) + j2];
        copiedBoard[(i2 * n) + j2] = tempTileValue;
        return copiedBoard;
    }

    // a board that is obtained by exchanging any pair of tiles
    public Board twin() {
        int[] copiedTiles = tiles.clone();

        if (copiedTiles[0] != 0 && copiedTiles[1] != 0)
            return new Board(swapTwoTiles(0, 0, 0, 1));
        return new Board(swapTwoTiles(1, 0, 1, 1));
    }

    public static void main(String[] args) {
        int[] tilesIn = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 0, 65, 67, 68, 69, 70, 72, 73, 74, 66, 75, 76, 77, 79, 71, 80}; // {1, 0, 2, 3}; // {1, 2, 3, 4, 5, 6, 7, 8, 0};
        Board b = new Board(tilesIn);

        //System.out.println(b.toString());
        //b = b.twin();
        //System.out.println(b.toString());

        System.out.println(b.equals(new Board(tilesIn)));
    }

}