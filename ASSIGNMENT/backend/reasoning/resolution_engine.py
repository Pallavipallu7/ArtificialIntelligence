from typing import List, Tuple, Set, Dict, Any
from backend.reasoning.cnf import Clause, rule_to_cnf, fact_to_cnf
from backend.reasoning.kb import KnowledgeBase

def resolve_clauses(c1: Clause, c2: Clause) -> List[Clause]:
    """
    Performs propositional resolution on two clauses C1 and C2.
    Returns list of resolvent clauses.
    """
    resolvents = []
    for lit in c1.literals:
        neg_lit = lit[1:] if lit.startswith("~") else f"~{lit}"
        if neg_lit in c2.literals:
            new_literals = (c1.literals - {lit}) | (c2.literals - {neg_lit})
            resolvents.append(Clause(new_literals))
    return resolvents

def run_resolution_proof(kb: KnowledgeBase, facts: Dict[str, Any], query_consequent: str) -> Tuple[bool, List[str], List[Clause]]:
    """
    Performs resolution refutation for facts + KB -> query_consequent.
    Adds ~query_consequent and resolves until [] is derived or no new clauses can be formed.
    """
    clauses = []
    trace = []

    # 1. Add rule CNF clauses
    for rule in kb.get_active_rules():
        c = rule_to_cnf(rule.antecedents, rule.consequent)
        clauses.append(c)
        trace.append(f"KB Rule Clause [{rule.rule_id}]: {c}")

    # 2. Add fact unit clauses
    for k, v in facts.items():
        if k in ["diagnosed_cause", "symptoms"]:
            continue
        c = fact_to_cnf(k, v)
        clauses.append(c)
        trace.append(f"Fact Clause: {c}")

    # 3. Add negated query goal
    target_lit = query_consequent.lower().replace(" ", "_")
    negated_goal = Clause({f"~{target_lit}"})
    clauses.append(negated_goal)
    trace.append(f"Negated Goal Clause: {negated_goal}")

    # 4. Perform resolution loop
    clause_set = set(clauses)
    new_clauses = set()
    step = 0

    while step < 50:
        step += 1
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
        derived_in_pass = False

        for c1, c2 in pairs:
            resolvents = resolve_clauses(c1, c2)
            for res in resolvents:
                if res.is_empty():
                    trace.append(f"Step {step}: Resolved '{c1}' AND '{c2}' ---> Derived EMPTY CLAUSE [] (PROVED)")
                    return True, trace, list(clause_set)
                if res not in clause_set and res not in new_clauses:
                    new_clauses.add(res)
                    derived_in_pass = True
                    trace.append(f"Step {step}: Resolved '{c1}' AND '{c2}' ---> Derived '{res}'")

        if not derived_in_pass:
            break
        clauses.extend(list(new_clauses))
        clause_set.update(new_clauses)
        new_clauses.clear()

    trace.append("Resolution finished: Goal could not be refuted.")
    return False, trace, list(clause_set)
