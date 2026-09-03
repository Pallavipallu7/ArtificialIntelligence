import numpy as np
import random
from typing import Dict, Any, List
from backend.routing.environment import HelpdeskRoutingEnv, DEFAULT_STAFF_MEMBERS
from backend.routing.q_learning_agent import QLearningRoutingAgent
from backend.config import Q_LEARNING_EPISODES

def train_q_learning_routing_agent(episodes: int = Q_LEARNING_EPISODES) -> Tuple[QLearningRoutingAgent, List[Dict[str, Any]]]:
    env = HelpdeskRoutingEnv()
    agent = QLearningRoutingAgent(num_actions=env.num_actions)

    history = []
    print(f"Starting Q-Learning Training for {episodes} episodes...")

    for ep in range(1, episodes + 1):
        env.reset_workloads()
        state = env.sample_state()
        total_reward = 0.0
        res_times = []
        imbalances = []

        # 10 assignment steps per episode
        for _ in range(10):
            action = agent.select_action(state, explore=True)
            next_state, reward, info = env.step(state, action)
            agent.update(state, action, reward, next_state)

            state = next_state
            total_reward += reward
            res_times.append(info["resolution_time"])
            imbalances.append(info["workload_imbalance"])

        agent.decay_epsilon()

        avg_reward = round(float(total_reward / 10), 2)
        avg_res_time = round(float(np.mean(res_times)), 2)
        avg_imbalance = round(float(np.mean(imbalances)), 2)

        history.append({
            "episode": ep,
            "reward": avg_reward,
            "avg_resolution_time": avg_res_time,
            "workload_imbalance": avg_imbalance,
            "epsilon": round(float(agent.epsilon), 4)
        })

    agent.save()
    print(f"Training completed. Final Episode Avg Reward: {history[-1]['reward']}")
    return agent, history

if __name__ == "__main__":
    train_q_learning_routing_agent()
