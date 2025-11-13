import random

N = 8
POP_SIZE = 100
GENERATIONS = 1000
MUTATION_RATE = 0.1

def heuristic(state):
    h = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                h += 1
    return h

def crossover(p1, p2):
    point = random.randint(0, N - 1)
    c1 = p1[:point] + p2[point:]
    c2 = p2[:point] + p1[point:]
    return c1, c2

def mutate(child):
    if random.random() < MUTATION_RATE:
        col = random.randint(0, N - 1)
        child[col] = random.randint(0, N - 1)

random.seed()
population = [[random.randint(0, N - 1) for _ in range(N)] for _ in range(POP_SIZE)]

for gen in range(GENERATIONS):
    population.sort(key=lambda ind: heuristic(ind))
    
    if heuristic(population[0]) == 0:
        print(f"Solution found at generation {gen}")
        break
    
    new_pop = []
    elite = POP_SIZE // 10
    new_pop.extend(population[:elite])
    
    while len(new_pop) < POP_SIZE:
        i1 = random.randint(0, elite - 1)
        i2 = random.randint(0, elite - 1)
        c1, c2 = crossover(population[i1], population[i2])
        mutate(c1)
        mutate(c2)
        new_pop.append(c1)
        if len(new_pop) < POP_SIZE:
            new_pop.append(c2)
    
    population = new_pop

print(f"Genetic Algorithm Solution (Heuristic={heuristic(population[0])}):")
print(population[0])
