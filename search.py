# Developed by Salim El Ghersse, Maria Chmite, and Mohamed Ouballouk
import util
import heapq

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    """
    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        state: Search state
        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take
        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def depthFirstSearch(problem):
    """Search the deepest nodes in the search tree first."""
    #states to be explored (LIFO). holds nodes in form (state, action)
    frontier = util.Stack()
    exploredNodes = []
    #define start node
    startState = problem.getStartState()
    startNode = (startState, [])
    frontier.push(startNode)
    while not frontier.isEmpty():
        currentState, actions = frontier.pop()
        if currentState not in exploredNodes:
            exploredNodes.append(currentState)
            if problem.isGoalState(currentState):
                return actions
            else:
                successors = problem.getSuccessors(currentState)
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newNode = (succState, newAction)
                    frontier.push(newNode)
    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    frontier = util.Queue()
    exploredNodes = []
    startState = problem.getStartState()
    startNode = (startState, [], 0)  # (state, action, cost)
    frontier.push(startNode)
    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()
        if currentState not in exploredNodes:
            exploredNodes.append(currentState)
            if problem.isGoalState(currentState):
                return actions
            else:
                successors = problem.getSuccessors(currentState)
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)
                    frontier.push(newNode)
    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    frontier = util.PriorityQueue()
    exploredNodes = {}
    startState = problem.getStartState()
    startNode = (startState, [], 0)  # (state, action, cost)
    frontier.push(startNode, 0)
    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()
        if (currentState not in exploredNodes) or (currentCost < exploredNodes[currentState]):
            exploredNodes[currentState] = currentCost
            if problem.isGoalState(currentState):
                return actions
            else:
                successors = problem.getSuccessors(currentState)
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)
                    frontier.update(newNode, newCost)
    return actions
def nullHeuristic(state, problem=None):
    """ 
    
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem. This heuristic is trivial.
    """
    return 0
def misplacedTiles(state):
    """
    Heuristic: Returns the number of misplaced tiles in the 16-puzzle.
    """
    misplaced = 0
    goal = 1  # The goal starts with 1 and increments for each position
    for row in range(4):
        for col in range(4):
            if state.cells[row][col] != goal and state.cells[row][col] != 0:
                misplaced += 1
            goal += 1
            if goal == 16:
                goal = 0  # The last space is the blank (0)
    return misplaced
import math

def euclideanDistance(state):
    """
    Heuristic: Returns the sum of Euclidean distances of the tiles from their goal positions.
    """
    totalDistance = 0
    goal_positions = {
        1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3),
        5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (1, 3),
        9: (2, 0), 10: (2, 1), 11: (2, 2), 12: (2, 3),
        13: (3, 0), 14: (3, 1), 15: (3, 2)
    }

    for row in range(4):
        for col in range(4):
            tile = state.cells[row][col]
            if tile != 0:
                goal_row, goal_col = goal_positions[tile]
                distance = math.sqrt((goal_row - row) ** 2 + (goal_col - col) ** 2)
                totalDistance += distance

    return totalDistance
def manhattanDistance(state):
    """
    Heuristic: Returns the sum of Manhattan distances of the tiles from their goal positions.
    """
    totalDistance = 0
    goal_positions = {
        1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3),
        5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (1, 3),
        9: (2, 0), 10: (2, 1), 11: (2, 2), 12: (2, 3),
        13: (3, 0), 14: (3, 1), 15: (3, 2)
    }

    for row in range(4):
        for col in range(4):
            tile = state.cells[row][col]
            if tile != 0:  # Skip the blank tile
                goal_row, goal_col = goal_positions[tile]
                totalDistance += abs(goal_row - row) + abs(goal_col - col)
    return totalDistance
def outOfRowAndColumn(state):
    """
    Heuristic: Returns the sum of the number of tiles out of row and out of column.
    """
    out_of_row = 0
    out_of_column = 0
    goal_positions = {
        1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3),
        5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (1, 3),
        9: (2, 0), 10: (2, 1), 11: (2, 2), 12: (2, 3),
        13: (3, 0), 14: (3, 1), 15: (3, 2)
    }

    for row in range(4):
        for col in range(4):
            tile = state.cells[row][col]
            if tile != 0:  # Skip the blank tile
                goal_row, goal_col = goal_positions[tile]
                if row != goal_row:
                    out_of_row += 1
                if col != goal_col:
                    out_of_column += 1
    return out_of_row + out_of_column





'''def aStarSearch(problem, heuristic=misplacedTiles):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    exploredNodes = []
    startState = problem.getStartState()
    startNode = (startState, [], 0)
    frontier.push(startNode, 0)

    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()

        if problem.isGoalState(currentState):
            return actions

        if currentState not in exploredNodes:
            exploredNodes.append(currentState)

            for succState, succAction, succCost in problem.getSuccessors(currentState):
                newActions = actions + [succAction]
                newCost = currentCost + succCost
                totalCost = newCost + heuristic(succState)  # Add heuristic
                frontier.push((succState, newActions, newCost), totalCost)

    return []'''

def aStarSearch(problem, heuristic):
    # Priority queue for the fringe
    fringe = []
    count = 0  # Unique counter for each state, to break ties in the heap

    # Push the start state to the fringe with priority 0
    heapq.heappush(fringe, (0, count, problem.getStartState(), [], 0))  # (priority, count, state, actions, cost)

    # Sets to track visited states
    closed = set()

    # Tracking variables
    expanded_nodes = 0
    max_fringe_size = 1
    solution_depth = 0

    while fringe:
        # Update max fringe size
        max_fringe_size = max(max_fringe_size, len(fringe))

        # Get the node with the lowest priority
        _, _, state, actions, cost = heapq.heappop(fringe)

        # Check if we've reached the goal
        if problem.isGoalState(state):
            solution_depth = len(actions)  # Depth is the number of actions taken
            return actions, expanded_nodes, max_fringe_size, solution_depth

        # If state has not been visited, expand it
        if state not in closed:
            closed.add(state)
            expanded_nodes += 1  # Increment the expanded nodes counter

            # Expand successors
            for successor, action, step_cost in problem.getSuccessors(state):
                if successor not in closed:
                    new_actions = actions + [action]
                    new_cost = cost + step_cost
                    priority = new_cost + heuristic(successor)  # f(n) = g(n) + h(n)
                    count += 1
                    heapq.heappush(fringe, (priority, count, successor, new_actions, new_cost))

    return [], expanded_nodes, max_fringe_size, solution_depth  # If no solution is found, return empty path


