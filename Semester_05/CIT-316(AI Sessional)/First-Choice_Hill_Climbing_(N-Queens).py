import random

N = 8

def heuristic(state):
    h = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                h += 1
    return h

def first_choice_hc(state, max_trials=50):
    while True:
        improved = False
        h_current = heuristic(state)
        
        for t in range(max_trials):
            col = random.randint(0, N - 1)
            row = random.randint(0, N - 1)
            if row == state[col]:
                continue
            
            new_state = state[:]
            new_state[col] = row
            
            h_new = heuristic(new_state)
            if h_new < h_current:
                state = new_state
                improved = True
                break
        
        if not improved:
            break
    
    return state

random.seed()
state = [random.randint(0, N - 1) for _ in range(N)]

solution = first_choice_hc(state)
print(f"First-Choice Hill Climbing Solution (Heuristic={heuristic(solution)}):")
print(solution)
