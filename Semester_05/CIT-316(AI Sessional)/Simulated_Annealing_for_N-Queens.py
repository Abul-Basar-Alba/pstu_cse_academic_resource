import random
import math

N = 8

def heuristic(state):
    h = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                h += 1
    return h

def simulated_annealing(T=1000, cooling=0.99):
    state = [random.randint(0, N - 1) for _ in range(N)]
    
    while T > 1e-3:
        col = random.randint(0, N - 1)
        row = random.randint(0, N - 1)
        new_state = state[:]
        new_state[col] = row
        
        delta = heuristic(new_state) - heuristic(state)
        if delta < 0 or random.random() < math.exp(-delta / T):
            state = new_state
        
        T *= cooling
        if heuristic(state) == 0:
            break
    
    return state

random.seed()
solution = simulated_annealing()
print(f"Simulated Annealing Solution (Heuristic={heuristic(solution)}):")
print(solution)
