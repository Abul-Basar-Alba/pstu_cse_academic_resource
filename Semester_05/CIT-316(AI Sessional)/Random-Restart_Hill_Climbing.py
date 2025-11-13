import random

N = 8

def heuristic(state):
    h = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                h += 1
    return h

def hill_climb(state):
    while True:
        current_h = heuristic(state)
        best_state = state[:]
        best_h = current_h
        
        for col in range(N):
            original_row = state[col]
            for row in range(N):
                if row == original_row:
                    continue
                state[col] = row
                h = heuristic(state)
                if h < best_h:
                    best_h = h
                    best_state = state[:]
            state[col] = original_row
        
        if best_h >= current_h:
            break
        state = best_state[:]
    
    return state

def random_restart_hc(restarts=1000):
    best_state = None
    best_h = float('inf')
    
    for r in range(restarts):
        state = [random.randint(0, N - 1) for _ in range(N)]
        sol = hill_climb(state)
        h = heuristic(sol)
        if h < best_h:
            best_h = h
            best_state = sol
            if h == 0:
                break
    
    return best_state

random.seed()
solution = random_restart_hc()
print(f"Random-Restart Hill Climbing Solution (Heuristic={heuristic(solution)}):")
print(solution)
