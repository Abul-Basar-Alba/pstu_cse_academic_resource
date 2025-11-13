import random

N = 8

def heuristic(state):
    h = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                h += 1
    return h

def print_board(state):
    for row in range(N):
        for col in range(N):
            print('Q' if state[col] == row else '.', end=' ')
        print()
    print()

def hill_climb(state):
    iteration = 0
    
    while True:
        iteration += 1
        current_h = heuristic(state)
        
        print(f"Iteration {iteration}: State {state} (Conflicts: {current_h})")
        
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
            print(f"No better neighbor. Final conflicts: {current_h}")
            if current_h == 0:
                print("SUCCESS! Solution found.")
            else:
                print(f"STUCK at local optimum with {current_h} conflicts.")
            break
        
        print(f"Better state found! Moving from h={current_h} to h={best_h}")
        state = best_state[:]
    
    return state

random.seed(42)
state = [random.randint(0, N-1) for _ in range(N)]

print("INITIAL STATE:")
print(f"State: {state} (Conflicts: {heuristic(state)})")
print_board(state)

print("\nHILL CLIMBING START\n")
solution = hill_climb(state)

print("\nGOAL STATE:")
print(f"State: {solution} (Conflicts: {heuristic(solution)})")
print_board(solution)
