import pytest
from backend.reasoning.kb import KnowledgeBase, Rule
from backend.reasoning.forward_chaining import forward_chain
from backend.reasoning.backward_chaining import backward_chain
from backend.reasoning.consistency import detect_contradictions, detect_circular_dependencies
from backend.services.diagnosis_service import diagnose_symptoms, clear_diagnosis_cache

def test_tc01_valid_ac_report_power_supply_failure():
    """TC01: Valid AC report -> Power supply failure."""
    kb = KnowledgeBase()
    symptoms = {"power_indicator": "off", "remote_no_response": True}
    diagnosis, confidence, proof_trace, _ = forward_chain(kb, symptoms)
    assert diagnosis == "Power supply failure"
    assert confidence >= 0.85
    assert len(proof_trace) > 0
    assert proof_trace[0]["matched_rule"] == "R1"

def test_tc02_insufficient_symptoms_clarification_question():
    """TC02: Insufficient symptoms -> clarification question generated via backward chaining."""
    kb = KnowledgeBase()
    incomplete_symptoms = {"power_indicator": "on"}
    diagnosis, _, _, _ = forward_chain(kb, incomplete_symptoms)
    assert diagnosis is None

    missing_facts, questions, candidates = backward_chain(kb, incomplete_symptoms)
    assert len(missing_facts) > 0
    assert len(questions) > 0
    assert any("compressor" in q.lower() or "remote" in q.lower() or "cooling" in q.lower() for q in questions)

def test_tc03_contradictory_rules_inconsistency_detected():
    """TC03: Contradictory rules -> inconsistency detected."""
    kb = KnowledgeBase()
    kb.add_rule(Rule(
        rule_id="R_TEST_CONTRADICT",
        category="AC_POWER",
        antecedents={"power_indicator": "off", "remote_no_response": True},
        consequent="Blown Internal Fuse",
        priority=10
    ))
    symptoms = {"power_indicator": "off", "remote_no_response": True}
    contradictions = detect_contradictions(kb, symptoms)
    assert len(contradictions) > 0
    assert contradictions[0]["type"] == "CONTRADICTORY_CONCLUSIONS"

def test_tc11_identical_diagnosis_twice_cached():
    """TC11: Identical diagnosis twice -> cached second result."""
    clear_diagnosis_cache()
    symptoms = {"power_indicator": "off", "remote_no_response": True}
    res1 = diagnose_symptoms(symptoms)
    assert res1["cached"] is False

    res2 = diagnose_symptoms(symptoms)
    assert res2["cached"] is True
    assert res2["diagnosis"] == res1["diagnosis"]

def test_tc12_circular_rules_terminate_safely():
    """TC12: Circular rules -> engine terminates safely."""
    kb = KnowledgeBase()
    kb.rules = [
        Rule("R_LOOP_1", "LOOP", {"fact_a": True}, "fact_b", priority=1),
        Rule("R_LOOP_2", "LOOP", {"fact_b": True}, "fact_a", priority=1)
    ]
    symptoms = {"fact_a": True}
    diagnosis, confidence, proof_trace, _ = forward_chain(kb, symptoms, max_iterations=5)
    # Engine should terminate gracefully without Infinite Loop recursion error
    assert proof_trace is not None
