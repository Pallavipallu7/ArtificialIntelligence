# Experiment 37: Genetic Algorithm for Function Optimization

import numpy as np

# Objective Function to Maximize: f(x) = -(x - 5)^2 + 25 (Peak at x = 5, Max Value = 25)
def fitness_function(x):
    return -(x - 5)**2 + 25

# Genetic Algorithm Parameters
POP_SIZE = 10
GENS = 15
MUTATION_RATE = 0.1

# Initialize Population (random values between 0 and 10)
population = np.random.uniform(0, 10, POP_SIZE)

print("=== GENETIC ALGORITHM FOR MATHEMATICAL OPTIMIZATION ===")
print("Objective Function: Maximize f(x) = -(x - 5)^2 + 25")
print(f"Population Size: {POP_SIZE} | Generations: {GENS}")
print("-" * 55)

for gen in range(1, GENS + 1):
    fitness = fitness_function(population)
    best_idx = np.argmax(fitness)
    best_x = population[best_idx]
    best_fit = fitness[best_idx]

    # Selection (Tournament)
    selected = []
    for _ in range(POP_SIZE):
        i, j = np.random.choice(POP_SIZE, 2, replace=False)
        selected.append(population[i] if fitness[i] > fitness[j] else population[j])
    
    # Crossover & Mutation
    next_gen = []
    for i in range(0, POP_SIZE, 2):
        parent1, parent2 = selected[i], selected[i+1]
        child1 = 0.5 * parent1 + 0.5 * parent2 # Arithmetic Crossover
        child2 = 0.7 * parent1 + 0.3 * parent2
        
        # Mutation
        if np.random.rand() < MUTATION_RATE:
            child1 += np.random.normal(0, 0.5)
        if np.random.rand() < MUTATION_RATE:
            child2 += np.random.normal(0, 0.5)
            
        next_gen.extend([child1, child2])
        
    population = np.clip(next_gen, 0, 10)
    
    if gen % 3 == 0 or gen == GENS:
        print(f"Generation {gen:02d}: Best x = {best_x:.4f} | Max Fitness = {best_fit:.4f}")

print("-" * 55)
print(f"OPTIMAL SOLUTION FOUND: x = {best_x:.4f} with Value = {best_fit:.4f}")
