import random

N = 8

def heuristic(state):
    h = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                h += 1
    return h

def stochastic_hc(state):
    while True:
        current_h = heuristic(state)
        improving_moves = []
        
        for col in range(N):
            original_row = state[col]
            for row in range(N):
                if row == original_row:
                    continue
                state[col] = row
                h = heuristic(state)
                if h < current_h:
                    improving_moves.append((col, row))
            state[col] = original_row
        
        if not improving_moves:
            break
        
        move = random.choice(improving_moves)
        state[move[0]] = move[1]
    
    return state

random.seed()
state = [random.randint(0, N - 1) for _ in range(N)]

solution = stochastic_hc(state)
print(f"Stochastic Hill Climbing Solution (Heuristic={heuristic(solution)}):")
print(solution)
