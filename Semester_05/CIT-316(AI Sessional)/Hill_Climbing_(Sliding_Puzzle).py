# Hill Climbing with Simulated Annealing fallback for 8-Puzzle
import random
import math
import copy

class Puzzle:
    def __init__(self, board):
        self.board = [row[:] for row in board]
        self.h = self.calculate_heuristic()
    
    def calculate_heuristic(self):
        # Count misplaced tiles (excluding blank)
        goal = [[1,2,3],[4,5,6],[7,8,0]]
        h = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0 and self.board[i][j] != goal[i][j]:
                    h += 1
        return h
    
    def is_goal(self):
        return self.h == 0

def get_neighbors(p):
    neighbors = []
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    # Find blank position
    x, y = 0, 0
    for i in range(3):
        for j in range(3):
            if p.board[i][j] == 0:
                x, y = i, j
                break
    
    # Generate all possible moves
    for k in range(4):
        nx, ny = x + dx[k], y + dy[k]
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_board = [row[:] for row in p.board]
            new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
            neighbors.append(Puzzle(new_board))
    
    return neighbors

def hill_climbing(start):
    current = start
    steps = 0
    
    while steps < 100:
        steps += 1
        
        if current.is_goal():
            print(f"Hill Climbing: Goal reached in {steps} steps!")
            return current, True
        
        neighbors = get_neighbors(current)
        best = min(neighbors, key=lambda x: x.h)
        
        # If no improvement, stuck at local maximum
        if best.h >= current.h:
            print(f"Hill Climbing: Stuck at local maximum (h={current.h}) after {steps} steps")
            return current, False
        
        current = best
    
    print("Hill Climbing: Max steps reached")
    return current, False

def simulated_annealing(start, max_iterations=50000):
    current = start
    temperature = 1000.0
    cooling_rate = 0.9995
    steps = 0
    
    print("\nSwitching to Simulated Annealing...")
    
    while temperature > 0.01 and steps < max_iterations:
        steps += 1
        
        if current.is_goal():
            print(f"Simulated Annealing: Goal reached in {steps} steps!")
            return current, True
        
        # Get random neighbor
        neighbors = get_neighbors(current)
        next_state = random.choice(neighbors)
        
        delta_h = next_state.h - current.h
        
        # Accept better states or worse states with probability
        if delta_h < 0 or random.random() < math.exp(-delta_h / temperature):
            current = next_state
        
        temperature *= cooling_rate
        
        # Progress update every 5000 steps
        if steps % 5000 == 0:
            print(f"Step {steps}: h={current.h}, temp={temperature:.2f}")
    
    if current.is_goal():
        print(f"Simulated Annealing: Goal reached in {steps} steps!")
        return current, True
    else:
        print(f"Simulated Annealing: Did not reach goal (h={current.h})")
        return current, False

def print_board(p):
    for row in p.board:
        print(' '.join('_' if x == 0 else str(x) for x in row))

# Initial state from problem: 3 8 5 / _ 7 1 / 2 6 4
start_board = [
    [3, 8, 5],
    [0, 7, 1],
    [2, 6, 4]
]

print("8-Puzzle Solver - Hill Climbing with Simulated Annealing Fallback\n")

print("Initial State (h=8):")
start = Puzzle(start_board)
print_board(start)

print(f"\nGoal State:\n1 2 3\n4 5 6\n7 8 _\n")

solution, solved = hill_climbing(start)

# If Hill Climbing fails, try Simulated Annealing multiple times
if not solved:
    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        print(f"\n--- Simulated Annealing Attempt {attempt}/{max_attempts} ---")
        solution, solved = simulated_annealing(start)
        if solved:
            break

print(f"\nFinal State (h={solution.h}):")
print_board(solution)

if solved:
    print("\nSuccess! Goal state reached.")
else:
    print("\nNote: This configuration is very difficult for Hill Climbing.")
