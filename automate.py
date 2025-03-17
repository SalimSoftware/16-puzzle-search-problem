import csv
from SixteenPuzzlestate import SixteenPuzzleState, SixteenPuzzleSearchProblem
from search import aStarSearch, misplacedTiles, euclideanDistance, manhattanDistance, outOfRowAndColumn
from statistics import mean
from multiprocessing import Process, Queue
import time
import random
from tabulate import tabulate  # Make sure you have installed this library using pip install tabulate

# In run_search_algorithm function, ensure the result queue is populated with proper data
def run_search_algorithm(problem, heuristic_function, result_queue):
    """
    Function to run the search algorithm and put the result in the queue.
    """
    start_time = time.time()
    path, nodes_expanded, max_fringe_size, depth = aStarSearch(problem, heuristic_function)
    end_time = time.time()
    execution_time = end_time - start_time
    # Add execution time to the result and store it in the queue
    result_queue.put((path, nodes_expanded, max_fringe_size, depth, execution_time))


def generate_random_puzzles(filename, num_puzzles=20):
    """
    Generate random puzzle configurations and save them to a file.
    """
    with open(filename, 'w') as file:
        for _ in range(num_puzzles):
            puzzle = SixteenPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])  # Start with a solved puzzle
            puzzle = create_random_moves(puzzle, 25)  # Apply 25 random moves to shuffle the puzzle
            config = [puzzle.cells[row][col] for row in range(4) for col in range(4)]  # Flatten the puzzle grid
            config_str = ' '.join(map(str, config))
            file.write(config_str + '\n')

def create_random_moves(puzzle, num_moves):
    """
    Create a random puzzle by applying random legal moves to the given puzzle.
    """
    for _ in range(num_moves):
        move = random.choice(puzzle.legalMoves())  # Choose a random legal move
        puzzle = puzzle.result(move)  # Apply the move to the puzzle
    return puzzle

def read_puzzle_configurations(filename):
    """
    Read puzzle configurations from a file.
    """
    configurations = []
    with open(filename, 'r') as file:
        for line in file:
            config = [int(n) for n in line.strip().split()]
            configurations.append(config)
    return configurations

def main():
    # Step 1: Generate random puzzles and save them to scenarios.csv
    generate_random_puzzles('scenarios.csv', num_puzzles=20)

    # Step 2: Read the puzzle configurations from scenarios.csv
    configurations = read_puzzle_configurations('scenarios.csv')
    
    # Define the heuristics we want to test
    heuristics = [misplacedTiles, euclideanDistance, manhattanDistance, outOfRowAndColumn]
    
    # Create a dictionary to store results for each heuristic
    results = {heuristic.__name__: {'Nodes Expanded': [], 'Max Fringe Size': [], 'Execution Time': []} for heuristic in heuristics}

    timeout = 120  # Adjust the timeout based on puzzle complexity

    # Step 3: Write results to results.csv
    with open('results.csv', 'w', newline='') as results_file:
        results_writer = csv.writer(results_file)
        results_writer.writerow(['Initial State', 'Heuristic', 'Expanded Nodes', 'Max Fringe Size', 'Depth', 'Execution Time'])

        for config in configurations:
            puzzle = SixteenPuzzleState(config)  # Initialize the puzzle with the current configuration
            problem = SixteenPuzzleSearchProblem(puzzle)  # Create a search problem instance

            for heuristic_function in heuristics:
                result_queue = Queue()
                process = Process(target=run_search_algorithm, args=(problem, heuristic_function, result_queue))
                process.start()

                # Wait for the process to finish or timeout
                process.join(timeout)

                if process.is_alive():
                    print(f"Timeout occurred for configuration {config} with heuristic {heuristic_function.__name__}")
                    process.terminate()
                    process.join()
                    results_writer.writerow([' '.join(map(str, config)), heuristic_function.__name__, "Timeout", "Timeout", "Timeout", "Timeout"])
                else:
                    if result_queue.empty():
                        print(f"No result found for {config} and {heuristic_function.__name__}")
                    else:
                        path, nodes_expanded, max_fringe_size, depth, execution_time = result_queue.get()
                        results[heuristic_function.__name__]['Nodes Expanded'].append(nodes_expanded)
                        results[heuristic_function.__name__]['Max Fringe Size'].append(max_fringe_size)
                        results[heuristic_function.__name__]['Execution Time'].append(execution_time)
                        results_writer.writerow([' '.join(map(str, config)), heuristic_function.__name__, nodes_expanded, max_fringe_size, depth, execution_time])

    # Step 4: Calculate averages from the results
    averages = {heuristic: {
        'Avg Nodes Expanded': mean(metrics['Nodes Expanded']),
        'Avg Max Fringe Size': mean(metrics['Max Fringe Size']),
        'Avg Execution Time': mean(metrics['Execution Time'])
    } for heuristic, metrics in results.items()}

    # Step 5: Rank heuristics based on average nodes expanded
    ranked_heuristics = sorted(averages.keys(), key=lambda x: averages[x]['Avg Nodes Expanded'])

    # Step 6: Display the average results using tabulate
    headers = ["Heuristic", "Avg Nodes Expanded", "Avg Max Fringe Size", "Avg Execution Time"]
    rows = [[heuristic, averages[heuristic]['Avg Nodes Expanded'], averages[heuristic]['Avg Max Fringe Size'], averages[heuristic]['Avg Execution Time']] for heuristic in ranked_heuristics]
    print("\nAverage Results:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()
