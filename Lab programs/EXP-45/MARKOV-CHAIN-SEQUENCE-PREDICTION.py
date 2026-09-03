# Experiment 45: Markov Chain Model for Predicting Sequences of Events

import numpy as np

# States: 0 = Sunny, 1 = Rainy, 2 = Cloudy
states = ["Sunny", "Rainy", "Cloudy"]

# Transition Probability Matrix P (P[i][j] = Prob of transitioning from state i to state j)
P = np.array([
    [0.6, 0.2, 0.2],  # From Sunny
    [0.3, 0.4, 0.3],  # From Rainy
    [0.2, 0.3, 0.5]   # From Cloudy
])

# Predict weather sequence over 7 days starting from Sunny (State 0)
current_state = 0
sequence = [states[current_state]]

np.random.seed(42)
for day in range(1, 7):
    current_state = np.random.choice([0, 1, 2], p=P[current_state])
    sequence.append(states[current_state])

print("=== MARKOV CHAIN SEQUENCE PREDICTION MODEL ===")
print("State Transition Probability Matrix:")
print(P)

print("\nSimulated 7-Day Sequence Prediction:")
for day, weather in enumerate(sequence):
    print(f"  Day {day+1}: {weather}")

# Calculate Steady-State Distribution
eigenvals, eigenvecs = np.linalg.eig(P.T)
stationary = eigenvecs[:, np.isclose(eigenvals, 1.0)].flatten()
stationary = stationary / np.sum(stationary)

print("\nLong-Term Steady State Probabilities:")
for i, state in enumerate(states):
    print(f"  P({state}): {stationary[i].real:.4f}")
