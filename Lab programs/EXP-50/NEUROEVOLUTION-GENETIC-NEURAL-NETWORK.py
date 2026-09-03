# Experiment 50: Genetic Algorithm to Evolve Neural Network (Neuroevolution)

import numpy as np

# Evolving weights of a Neural Network to solve XOR problem
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([0, 1, 1, 0])

POP_SIZE = 20
GENS = 50
num_weights = 2*4 + 4*1 # Architecture: 2 inputs -> 4 hidden -> 1 output (12 total weights)

# Initialize population of network weight vectors
population = np.random.randn(POP_SIZE, num_weights)

def forward(weights, x):
    W1 = weights[:8].reshape(2, 4)
    W2 = weights[8:].reshape(4, 1)
    h = np.maximum(0, np.dot(x, W1)) # ReLU
    out = 1 / (1 + np.exp(-np.dot(h, W2))) # Sigmoid
    return out.flatten()

print("=== NEUROEVOLUTION: GENETIC ALGORITHM EVOLVING NEURAL NETWORK ===")
print("Task: Learn XOR Logic Gate via Neural Network Weight Evolution")
print(f"Network Architecture: Input(2) -> Hidden(4, ReLU) -> Output(1, Sigmoid)")
print("-" * 65)

for gen in range(1, GENS + 1):
    scores = []
    for w in population:
        preds = forward(w, X)
        mse = np.mean((preds - y)**2)
        scores.append(1 / (1 + mse)) # Fitness is inverse MSE
        
    best_idx = np.argmax(scores)
    best_fitness = scores[best_idx]
    
    if gen % 10 == 0 or gen == GENS:
        print(f"Generation {gen:02d}: Best Population Fitness = {best_fitness:.4f}")
        
    # Tournament Selection & Mutation to evolve weights
    new_pop = [population[best_idx]]
    for _ in range(POP_SIZE - 1):
        parent = population[np.random.choice(POP_SIZE)]
        child = parent + np.random.randn(num_weights) * 0.2 # Mutation
        new_pop.append(child)
    population = np.array(new_pop)

best_weights = population[0]
final_preds = forward(best_weights, X)

print("-" * 65)
print("Final Evolved Network Predictions on XOR Inputs:")
for input_val, pred, target in zip(X, final_preds, y):
    print(f"  Input {input_val} -> Predicted: {pred:.4f} (Target: {target})")
print("STATUS: Neuroevolution Genetic Neural Network Training Complete!")
