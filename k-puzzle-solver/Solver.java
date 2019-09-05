import java.util.Stack;
import java.io.File;
import java.util.Scanner;
import java.util.PriorityQueue;
import java.io.FileNotFoundException;

public class Solver {

    private class Node implements Comparable<Node> {
        private final Board board;
        private final Node previousNode;
        private int numMoves;
        private final int manhattanValue;

        public Node(Board board, Node previousNode) {
            this.board = board;
            this.previousNode = previousNode;

            this.manhattanValue = board.manhattan(); // get manhattan calc value for the passed in board

            if (previousNode != null)
                numMoves = previousNode.numMoves + 1;
            else
                numMoves = 0;
        }

        @Override
        public int compareTo(Node that) {
            int priorityDifference = (this.manhattanValue + this.numMoves) - (that.manhattanValue + that.numMoves);
            if (priorityDifference == 0)
                return this.manhattanValue - that.manhattanValue;
            return priorityDifference;
        }
    }

    private boolean isSolvable;
    private final Stack<Board> solutions;

    public Solver(Board initial) {
        boolean solutionNotFound;
        if (initial == null)
            throw new IllegalArgumentException("Cannot pass in a null board");

        isSolvable = false;
        solutions = new Stack<>();

        // create new min priority queue of search nodes
        PriorityQueue<Node> searchNodes = new PriorityQueue<>();

        // add initial board state and a twin board state to this min PQ
        searchNodes.add(new Node(initial, null));
        searchNodes.add(new Node(initial.twin(), null));

        // check to see if initial board is goal
        solutionNotFound = !searchNodes.peek().board.isGoal();
        // find a solution by exploring further board possibilities
        while (solutionNotFound) {
            Node searchNode = searchNodes.poll(); // take the front node to explore
            // for each neighbouring board of the current search node:
            //  if the previous nodes board is not the current neighbouring board, explore deeper
            for (Board neighbouringBoard : searchNode.board.neighbors())
                if (searchNode.previousNode == null || (searchNode.previousNode!= null && !searchNode.previousNode.board.equals(neighbouringBoard)))
                    searchNodes.add(new Node(neighbouringBoard, searchNode));

            solutionNotFound = !searchNodes.peek().board.isGoal();
        }
        int[][] tiles = new int[n][n];
	        for (int i = 0; i < n; i++)
	            for (int j = 0; j < n; j++)
	                tiles[i][j] = in.nextInt();
	        Board initial = new Board(tiles);

	        // solve the puzzle
	        Solver solver = new Solver(initial);

	        // print solution to standard output
	        if (!solver.isSolvable())
	            System.out.println("No solution possible");
	        else {
	            System.out.println("Minimum number of moves = " + solver.moves());
	            for (Board board : solver.solution())
	                System.out.println(board);
	        }
        // retrieve solution
        Node currentNode = searchNodes.peek();
        // backtrack until we get to the first node
        while (currentNode.previousNode != null) {
            solutions.push(currentNode.board);
            currentNode = currentNode.previousNode;
        }
        solutions.push(currentNode.board);

        if (currentNode.board.equals(initial))
            isSolvable = true;
    }

    public boolean isSolvable() {
        return this.isSolvable;
    }

    public int moves() {
        if (!isSolvable())
            return -1;
        return solutions.size() - 1; // number of board states we go to until solution found
    }

    public Iterable<Board> solution() {
        if (isSolvable())
            return solutions;
        return null;
    }

    public static void main(String[] args) {
        // create initial board from file
        try {
        	Scanner in = new Scanner(new File("puzzle_text_files/p1.txt"));
        	int n = in.nextInt();
	        int[][] tiles = new int[n][n];
	        for (int i = 0; i < n; i++)
	            for (int j = 0; j < n; j++)
	                tiles[i][j] = in.nextInt();
	        Board initial = new Board(tiles);

	        // solve the puzzle
	        Solver solver = new Solver(initial);

	        // print solution to standard output
	        if (!solver.isSolvable())
	            System.out.println("No solution possible");
	        else {
	            System.out.println("Minimum number of moves = " + solver.moves());
	            for (Board board : solver.solution())
	                System.out.println(board);
	        }
        } catch(FileNotFoundException fnfe) { 
            System.out.println(fnfe.getMessage());
        } 
        
        
    }

}