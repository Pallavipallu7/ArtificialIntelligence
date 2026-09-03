# Experiment 43: Reinforcement Learning Q-Learning Agent

import numpy as np

# 4-State Grid Environment: S0 -> S1 -> S2 -> S3 (Goal)
# Actions: 0 = Left, 1 = Right
num_states = 4
num_actions = 2

# Q-Table Initialization
Q = np.zeros((num_states, num_actions))
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
episodes = 200

for ep in range(episodes):
    state = 0
    while state != 3:
        # Epsilon-greedy action selection
        action = 1 if np.random.rand() > 0.1 else np.random.choice([0, 1])
        next_state = min(3, state + 1) if action == 1 else max(0, state - 1)
        reward = 10 if next_state == 3 else -1
        
        # Q-Learning Bellman Update
        Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
        state = next_state

print("=== REINFORCEMENT LEARNING (Q-LEARNING AGENT) ===")
print("Environment: 4-State Line (S0=Start, S3=Goal)")
print(f"Episodes Trained: {episodes}")
print("Final Learned Q-Table (State x Action [Left, Right]):")
print(np.round(Q, 2))

print("\nDerived Optimal Policy:")
for s in range(num_states - 1):
    best_action = "RIGHT" if np.argmax(Q[s]) == 1 else "LEFT"
    print(f"  State S{s} -> Optimal Action: {best_action}")
