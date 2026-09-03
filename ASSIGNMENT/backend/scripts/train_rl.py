from backend.routing.train_agent import train_q_learning_routing_agent
from backend.routing.evaluate_agent import evaluate_routing_policies

def train_rl():
    print("--- Training Tabular Q-Learning Routing Agent ---")
    agent, history = train_q_learning_routing_agent(episodes=500)
    print("--- Evaluating Policy vs Baselines ---")
    eval_res = evaluate_routing_policies(agent)
    print("Q-Learning RL Agent Training & Evaluation Completed.")

if __name__ == "__main__":
    train_rl()
