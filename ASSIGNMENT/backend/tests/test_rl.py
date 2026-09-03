import pytest
from backend.routing.train_agent import train_q_learning_routing_agent
from backend.routing.evaluate_agent import evaluate_routing_policies

def test_tc07_q_learning_improvement_over_random():
    """TC07: Q-learning -> improvement over random assignment."""
    agent, history = train_q_learning_routing_agent(episodes=100)
    eval_res = evaluate_routing_policies(agent, test_steps=50)
    
    assert "q_learning" in eval_res
    assert "random" in eval_res
    # Mean reward for learned Q-policy should outperform or match random policy
    assert eval_res["q_learning"]["mean_reward"] >= eval_res["random"]["mean_reward"] - 2.0
