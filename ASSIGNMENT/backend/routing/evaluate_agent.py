import numpy as np
import random
from typing import Dict, Any
from backend.routing.environment import HelpdeskRoutingEnv, DEFAULT_STAFF_MEMBERS
from backend.routing.q_learning_agent import QLearningRoutingAgent

def evaluate_routing_policies(agent: QLearningRoutingAgent = None, test_steps: int = 200) -> Dict[str, Any]:
    """
    Compares Random, Round-Robin, and Q-Learning routing policy performance (TC07 compliance).
    """
    if agent is None:
        agent = QLearningRoutingAgent.load()

    env = HelpdeskRoutingEnv()

    # 1. Evaluate Random Assignment Policy
    env.reset_workloads()
    random_rewards, random_res_times, random_imbalances = [], [], []
    state = env.sample_state()
    for _ in range(test_steps):
        action = random.randint(0, env.num_actions - 1)
        next_state, reward, info = env.step(state, action)
        random_rewards.append(reward)
        random_res_times.append(info["resolution_time"])
        random_imbalances.append(info["workload_imbalance"])
        state = next_state

    # 2. Evaluate Round-Robin Policy
    env.reset_workloads()
    rr_rewards, rr_res_times, rr_imbalances = [], [], []
    state = env.sample_state()
    rr_index = 0
    for _ in range(test_steps):
        action = rr_index % env.num_actions
        rr_index += 1
        next_state, reward, info = env.step(state, action)
        rr_rewards.append(reward)
        rr_res_times.append(info["resolution_time"])
        rr_imbalances.append(info["workload_imbalance"])
        state = next_state

    # 3. Evaluate Q-Learning Policy (Exploration OFF)
    env.reset_workloads()
    ql_rewards, ql_res_times, ql_imbalances = [], [], []
    state = env.sample_state()
    for _ in range(test_steps):
        action = agent.select_action(state, explore=False) if agent else random.randint(0, env.num_actions - 1)
        next_state, reward, info = env.step(state, action)
        ql_rewards.append(reward)
        ql_res_times.append(info["resolution_time"])
        ql_imbalances.append(info["workload_imbalance"])
        state = next_state

    results = {
        "random": {
            "mean_reward": round(float(np.mean(random_rewards)), 2),
            "mean_resolution_time": round(float(np.mean(random_res_times)), 2),
            "workload_imbalance": round(float(np.mean(random_imbalances)), 2)
        },
        "round_robin": {
            "mean_reward": round(float(np.mean(rr_rewards)), 2),
            "mean_resolution_time": round(float(np.mean(rr_res_times)), 2),
            "workload_imbalance": round(float(np.mean(rr_imbalances)), 2)
        },
        "q_learning": {
            "mean_reward": round(float(np.mean(ql_rewards)), 2),
            "mean_resolution_time": round(float(np.mean(ql_res_times)), 2),
            "workload_imbalance": round(float(np.mean(ql_imbalances)), 2)
        },
        "improvement_over_random": round(float(np.mean(ql_rewards) - np.mean(random_rewards)), 2)
    }

    print(f"RL Policy Evaluation Complete. Improvement over Random: {results['improvement_over_random']}")
    return results

if __name__ == "__main__":
    evaluate_routing_policies()
