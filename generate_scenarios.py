import csv
import random

def createRandomSixteenPuzzle(moves=100):
    """
    Creates a random 16-puzzle by applying a number of random moves to a solved puzzle.
    """
    puzzle = list(range(16))  # Solved state
    random.shuffle(puzzle)
    return puzzle

def generate_scenarios(filename, num_scenarios=50):
    """
    Generates random 16-puzzle scenarios and writes them to a CSV file.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Scenario'])  # Header row

        for _ in range(num_scenarios):
            puzzle = createRandomSixteenPuzzle()
            writer.writerow([puzzle])

# Generate 50 random scenarios
generate_scenarios('scenarios.csv', num_scenarios=50)
