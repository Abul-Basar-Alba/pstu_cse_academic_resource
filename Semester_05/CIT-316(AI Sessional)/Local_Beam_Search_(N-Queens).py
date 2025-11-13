import random

N = 8

def heuristic(state):
    h = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                h += 1
    return h

def local_beam_search(k=3, max_iterations=100):
    states = [[random.randint(0, N - 1) for _ in range(N)] for _ in range(k)]
    
    for iteration in range(max_iterations):
        all_neighbors = []
        
        for state in states:
            for col in range(N):
                for row in range(N):
                    if row == state[col]:
                        continue
                    neighbor = state[:]
                    neighbor[col] = row
                    all_neighbors.append(neighbor)
        
        all_neighbors.sort(key=lambda s: heuristic(s))
        states = all_neighbors[:k]
        
        if heuristic(states[0]) == 0:
            break
    
    return states[0]

random.seed()
solution = local_beam_search()
print(f"Local Beam Search Solution (Heuristic={heuristic(solution)}):")
print(solution)
