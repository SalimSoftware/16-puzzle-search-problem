import search
import random


# Module Classes

class SixteenPuzzleState:
    """
    This class defines the mechanics of the 16-puzzle (4x4 grid).
    """

    def __init__(self, numbers):
        """
        Constructs a new 16-puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 15 representing an
        instance of the 16-puzzle. 0 represents the blank space.

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        self.cells = []
        numbers = numbers[:]  # Make a copy so as not to cause side-effects.
        numbers.reverse()
        for row in range(4):  # Update to 4 rows for 16-puzzle
            self.cells.append([])
            for col in range(4):  # Update to 4 columns for 16-puzzle
                self.cells[row].append(numbers.pop())
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal(self):
        """
        Checks to see if the puzzle is in its goal state.
        The goal state is:
            -------------
            |  1 |  2 |  3 |  4 |
            -------------
            |  5 |  6 |  7 |  8 |
            -------------
            |  9 | 10 | 11 | 12 |
            -------------
            | 13 | 14 | 15 |    |
            -------------
        """
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]   # we added this as a goal for it to be the obtained as the final state of the puzzle"""
        current = [] #We change from current = 0 to a list-based comparison (goal = [1, 2, 3, ..., 15, 0]) because the size of the puzzle increased, and it makes more sense to directly compare the current state of the 16-puzzle against the goal state by flattening the grid.
        for row in self.cells: # the new code flattens the entire 2D grid (a list of lists) into a single list using extend
            current.extend(row)
        return current == goal # By using current.extend(row), the entire puzzle state is transformed into a single list, and the comparison is straightforward:

    def legalMoves(self):
        """
        Returns a list of legal moves from the current state.
        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.
        """
        moves = []
        row, col = self.blankLocation
        if row != 0:
            moves.append('up')
        if row != 3:  # Update boundary for 4x4 grid
            moves.append('down')
        if col != 0:
            moves.append('left')
        if col != 3:  # Update boundary for 4x4 grid
            moves.append('right')
        return moves

    def result(self, move):
        """
        Returns a new SixteenPuzzleState with the current state and blankLocation
        updated based on the provided move.
        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception.
        """
        row, col = self.blankLocation
        if move == 'up':
            newrow = row - 1
            newcol = col
        elif move == 'down':
            newrow = row + 1
            newcol = col
        elif move == 'left':
            newrow = row
            newcol = col - 1
        elif move == 'right':
            newrow = row
            newcol = col + 1
        else:
            raise Exception("Illegal Move")

        # Create a copy of the current 16-puzzle
        newPuzzle = SixteenPuzzleState([0] * 16)  # Create empty 16-puzzle  it means an empty array full of 0'S
        newPuzzle.cells = [values[:] for values in self.cells]
        # Update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
        Overloads '==' such that two 16-puzzles with the same configuration
        are equal.
        """
        for row in range(4):  # Update to 4 rows for 16-puzzle
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
        Returns a display string for the puzzle.
        """
        lines = []
        horizontalLine = ('-' * (17))  # Adjust line length for 4x4 grid
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__().rjust(2) + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()


# Search Problem for the 16-puzzle

class SixteenPuzzleSearchProblem(search.SearchProblem):
    """
    Implementation of a SearchProblem for the 16 Puzzle domain.
    Each state is represented by an instance of a SixteenPuzzleState.
    """
    def __init__(self, puzzle):
        "Creates a new SixteenPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        """
        Returns list of (successor, action, stepCost) pairs where
        each successor is either left, right, up, or down
        from the original state and the cost is 1.0 for each.
        """
        successors = []
        for move in state.legalMoves():
            successors.append((state.result(move), move, 1))
        return successors

    def getCostOfActions(self, actions):
        """
        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        return len(actions)


# Helper function to create a random 16-puzzle

def createRandomSixteenPuzzle(moves=100):
    """
    moves: number of random moves to apply
    Creates a random 16-puzzle by applying
    a series of 'moves' random moves to a solved puzzle.
    """
    puzzle = SixteenPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])
    for i in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

def print_heuristic_menu():
    print("Please Choose a heuristic function for A* search:")
    print("1- h1 for number of misplaced tiles")
    print("2- h2 for sum of Euclidean distances of the tiles from their goal positions")
    print("3- h3 for sum of Manhattan distances of the tiles from their goal positions")
    print("4- h4 for Number of tiles out of row + Number of tiles out of column")

def get_heuristic_choice():
    choice = input("Choose heuristic: ")
    return choice

# Main execution

if __name__ == '__main__':
    puzzle = createRandomSixteenPuzzle(25)  # Initialize a random puzzle
    print('A random 16-puzzle:')
    print(puzzle)
    
    # Create the problem instance using the puzzle
    problem = SixteenPuzzleSearchProblem(puzzle)

    # Present the heuristic choices to the user
    print_heuristic_menu()
    choice = get_heuristic_choice()

    if choice == "1":
        print("You selected h1 (misplaced tiles heuristic).")
        path = search.aStarSearch(problem, heuristic=search.misplacedTiles)
        print('A* with misplacedTiles found a path of %d moves: %s' % (len(path), str(path)))
    elif choice == "2":
        print("You selected h2 (Euclidean distance heuristic).")
        path = search.aStarSearch(problem, heuristic=search.euclideanDistance)
        print('A* with euclideanDistance found a path of %d moves: %s' % (len(path), str(path)))
    elif choice == "3":
        print("You selected h3 (Manhattan distance heuristic).")
        path = search.aStarSearch(problem, heuristic=search.manhattanDistance)
        print('A* with manhattanDistance found a path of %d moves: %s' % (len(path), str(path)))
    elif choice == "4":
        print("You selected h4 (out of row and column heuristic).")
        path = search.aStarSearch(problem, heuristic=search.outOfRowAndColumn)
        print('A* with outOfRowAndColumn found a path of %d moves: %s' % (len(path), str(path)))
    else:
        print("Invalid choice.")

    # Simulate the puzzle solution after search
    # Simulate the puzzle solution after search
# Simulate the puzzle solution after search
    curr = puzzle
    i = 1

   # If 'path' is a tuple, it seems like the moves list is the first element in the tuple
# Extract the list of moves from the tuple if needed
    if isinstance(path, tuple):
     path = path[0]  # Take the first element which contains the moves

    for a in path:
     print(f"Current state before applying move '{a}':")
     print(curr)
     print(f"Legal moves available: {curr.legalMoves()}")

     if a not in curr.legalMoves():
        raise ValueError(f"Illegal move '{a}' detected. Exiting to prevent crash.")
    
     curr = curr.result(a)
     print('After %d move%s: %s' % (i, ("", "s")[i > 1], a))
     print(curr)
     input("Press return for the next state...")  # Wait for key press
     i += 1


