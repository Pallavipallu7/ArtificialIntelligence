import hashlib
import json
from typing import Dict, Any, Optional
from backend.reasoning.kb import KnowledgeBase
from backend.reasoning.forward_chaining import forward_chain
from backend.reasoning.backward_chaining import backward_chain
from backend.reasoning.cnf import rule_to_cnf, fact_to_cnf
from backend.reasoning.resolution_engine import run_resolution_proof
from backend.reasoning.explanation import build_explanation_trace

# Symptom hash diagnosis cache (TC11 compliance)
DIAGNOSIS_CACHE: Dict[str, Dict[str, Any]] = {}

def get_symptoms_hash(symptoms: Dict[str, Any]) -> str:
    norm_str = json.dumps(symptoms, sort_keys=True)
    return hashlib.md5(norm_str.encode('utf-8')).hexdigest()

def diagnose_symptoms(symptoms: Dict[str, Any], kb: Optional[KnowledgeBase] = None) -> Dict[str, Any]:
    if kb is None:
        kb = KnowledgeBase()

    sym_hash = get_symptoms_hash(symptoms)

    # Check cache (TC11 compliance)
    if sym_hash in DIAGNOSIS_CACHE:
        cached_res = DIAGNOSIS_CACHE[sym_hash].copy()
        cached_res["cached"] = True
        return cached_res

    # 1. Forward Chaining
    diagnosis, confidence, proof_trace, _ = forward_chain(kb, symptoms)

    # 2. Backward Chaining for missing symptoms
    missing_symptoms, questions, _ = backward_chain(kb, symptoms)

    # 3. CNF & Resolution trace calculation
    cnf_clause_str = None
    res_steps = []
    if diagnosis and proof_trace:
        rule_id = proof_trace[0]["matched_rule"]
        matched_rule = next((r for r in kb.get_active_rules() if r.rule_id == rule_id), None)
        if matched_rule:
            cnf_c = rule_to_cnf(matched_rule.antecedents, matched_rule.consequent)
            cnf_clause_str = str(cnf_c)
            _, res_steps, _ = run_resolution_proof(kb, symptoms, diagnosis)

    result = {
        "diagnosis": diagnosis,
        "confidence": confidence,
        "reasoning_method": "Forward Chaining (Rule-Based Expert System)",
        "proof_trace": proof_trace,
        "missing_symptoms": missing_symptoms,
        "cached": False,
        "cnf_clause": cnf_clause_str,
        "resolution_steps": res_steps[:10],
        "explanation": build_explanation_trace(symptoms, proof_trace, diagnosis, confidence)
    }

    # Store in cache
    DIAGNOSIS_CACHE[sym_hash] = result
    return result

def clear_diagnosis_cache():
    DIAGNOSIS_CACHE.clear()
