from SixteenPuzzlestate import SixteenPuzzleState, SixteenPuzzleSearchProblem, createRandomSixteenPuzzle
from search import breadthFirstSearch, depthFirstSearch, uniformCostSearch, aStarSearch, manhattanDistance
from prettytable import PrettyTable
from multiprocessing import Process, Queue
import time

def run_algorithm(algo_func, problem, heuristic, result_queue):
 # the function to run the search algorithm and put the result in a queue.

    start_time = time.time()
    if heuristic:
        result = algo_func(problem, heuristic)
    else:
        result = algo_func(problem)
    end_time = time.time()
    execution_time = end_time - start_time
    result_queue.put((result, execution_time))

def main():
    puzzle = createRandomSixteenPuzzle()
    problem = SixteenPuzzleSearchProblem(puzzle)

    print("Generated Random 16-Puzzle:")
    print(puzzle)

    algorithms = {
        'A* with heuristic3': (aStarSearch, manhattanDistance),
        'BFS': (breadthFirstSearch, None),
        'DFS': (depthFirstSearch, None),
        'UCS': (uniformCostSearch, None),

    }

    results = {}
    timeout = 10000  # Timeout 

    for algo_name, (algo_func, heuristic) in algorithms.items():
        result_queue = Queue()
        args = (algo_func, problem, heuristic, result_queue)

        # Create and start a process for the algorithm
        process = Process(target=run_algorithm, args=args)
        process.start()

        # Wait for the process to finish or timeout
        process.join(timeout)

        if process.is_alive():
            print(f"Timeout occurred for {algo_name}")
            process.terminate()
            process.join()
            results[algo_name] = {'Outcome': 'Timeout', 'Path Length': "N/A", 'Nodes Expanded': "N/A", 'Max Fringe Size': "N/A", 'Depth': "N/A", 'Execution time': "N/A"}
        else:
            (result, execution_time) = result_queue.get()
            path, nodes_expanded, max_fringe_size, depth = result
            results[algo_name] = {'Outcome': 'Completed', 'Path Length': len(path), 'Nodes Expanded': nodes_expanded, 'Max Fringe Size': max_fringe_size, 'Depth': depth, 'Execution time': f"{execution_time:.2f} sec"}

    # Display results in a table
    table = PrettyTable()
    table.field_names = ["Algorithm", "Outcome", "Path Length", "Nodes Expanded", "Max Fringe Size", "Depth", "Execution time"]
    for algo_name, metrics in results.items():
        table.add_row([algo_name, metrics['Outcome'], metrics['Path Length'], metrics['Nodes Expanded'], metrics['Max Fringe Size'], metrics['Depth'], metrics['Execution time']])
    print(table)
if __name__ == '__main__':
    main()