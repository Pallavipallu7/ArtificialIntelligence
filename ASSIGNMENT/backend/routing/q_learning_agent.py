import numpy as np
import random
import joblib
from pathlib import Path
from typing import Tuple, Dict, Any, List
from backend.config import MODEL_DIR

class QLearningRoutingAgent:
    def __init__(self, num_actions: int = 6, alpha: float = 0.1, gamma: float = 0.9, epsilon: float = 1.0, epsilon_decay: float = 0.995, min_epsilon: float = 0.05):
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.q_table: Dict[Tuple[str, str, str], np.ndarray] = {}

    def get_q_values(self, state: Tuple[str, str, str]) -> np.ndarray:
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.num_actions)
        return self.q_table[state]

    def select_action(self, state: Tuple[str, str, str], explore: bool = True) -> int:
        if explore and random.random() < self.epsilon:
            return random.randint(0, self.num_actions - 1)
        q_vals = self.get_q_values(state)
        return int(np.argmax(q_vals))

    def update(self, state: Tuple[str, str, str], action: int, reward: float, next_state: Tuple[str, str, str]):
        q_vals = self.get_q_values(state)
        next_q_vals = self.get_q_values(next_state)

        best_next_q = np.max(next_q_vals)
        td_target = reward + self.gamma * best_next_q
        td_error = td_target - q_vals[action]

        # Tabular Q-learning update rule
        q_vals[action] += self.alpha * td_error

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def save(self, file_path: Path = None):
        if file_path is None:
            file_path = MODEL_DIR / "q_table.pkl"
        joblib.dump({
            "q_table": self.q_table,
            "num_actions": self.num_actions,
            "epsilon": self.epsilon
        }, file_path)
        print(f"Saved Q-learning agent Q-table to {file_path}")

    @staticmethod
    def load(file_path: Path = None):
        if file_path is None:
            file_path = MODEL_DIR / "q_table.pkl"
        if not file_path.exists():
            return None
        data = joblib.load(file_path)
        agent = QLearningRoutingAgent(num_actions=data["num_actions"])
        agent.q_table = data["q_table"]
        agent.epsilon = data.get("epsilon", 0.05)
        return agent
