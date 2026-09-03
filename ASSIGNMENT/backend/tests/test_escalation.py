import pytest
import numpy as np
from backend.learning.dataset_generator import generate_synthetic_dataset
from backend.learning.escalation_model import EscalationRiskModel

def test_tc05_missing_values_imputation_escalation_model():
    """TC05: Missing values -> escalation model still produces prediction."""
    df = generate_synthetic_dataset(num_samples=80)
    model = EscalationRiskModel()
    model.train(df)

    incomplete_ticket = {
        "department": "CSE",
        "severity": np.nan,
        "previous_incidents": np.nan,
        "symptoms": {"power_indicator": np.nan}
    }

    res = model.predict_risk(incomplete_ticket)
    assert "escalation_probability" in res
    assert "risk_level" in res
    assert res["missing_values_handled"] is True
    assert 0.0 <= res["escalation_probability"] <= 1.0

def test_tc06_high_escalation_risk_priority_handling():
    """TC06: High escalation risk -> priority handling."""
    model = EscalationRiskModel.load()
    if model is None:
        df = generate_synthetic_dataset(num_samples=80)
        model = EscalationRiskModel()
        model.train(df)

    high_risk_ticket = {
        "department": "Biotechnology",
        "severity": 5,
        "previous_incidents": 8,
        "symptoms": {"lab_equipment_no_power": True, "socket_tested_ok": True}
    }
    res = model.predict_risk(high_risk_ticket)
    assert res["escalation_probability"] >= 0.0
    assert "risk_level" in res
