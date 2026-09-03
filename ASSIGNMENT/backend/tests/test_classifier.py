import pytest
from backend.learning.dataset_generator import generate_synthetic_dataset
from backend.learning.decision_tree import TicketDecisionTreeModel

def test_tc04_decision_tree_prediction():
    """TC04: Historical ticket -> Decision Tree prediction."""
    df = generate_synthetic_dataset(num_samples=100)
    dt_model = TicketDecisionTreeModel()
    metrics = dt_model.train(df)
    
    assert "category_accuracy" in metrics
    assert "priority_accuracy" in metrics
    assert "feature_importance" in metrics
    
    pred = dt_model.predict({
        "department": "CSE",
        "location": "CSE Lab 2",
        "symptoms": {"power_indicator": "off", "remote_no_response": True}
    })
    
    assert "category" in pred
    assert "priority" in pred
    assert pred["confidence"] >= 0.5
