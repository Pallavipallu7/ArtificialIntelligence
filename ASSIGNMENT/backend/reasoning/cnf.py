from typing import List, Dict, Any, Set

class Clause:
    """Represents a disjunction (OR) of literals, e.g. {'~power_off', '~remote_no_response', 'power_supply_failure'}"""
    def __init__(self, literals: Set[str]):
        self.literals = set(literals)

    def is_empty(self) -> bool:
        return len(self.literals) == 0

    def __repr__(self) -> str:
        if not self.literals:
            return "[] (EMPTY/CONTRADICTION)"
        return " v ".join(sorted(list(self.literals)))

    def __eq__(self, other) -> bool:
        if isinstance(other, Clause):
            return self.literals == other.literals
        return False

    def __hash__(self) -> int:
        return hash(frozenset(self.literals))

def rule_to_cnf(antecedents: Dict[str, Any], consequent: str) -> Clause:
    """
    Converts a rule A1 AND A2 ... -> C into CNF clause (~A1 v ~A2 v ... v C)
    """
    literals = set()
    for k, v in antecedents.items():
        if isinstance(v, bool):
            val_str = "true" if v else "false"
        else:
            val_str = str(v).lower()
        lit = f"~{k}={val_str}"
        literals.add(lit)

    cons_str = consequent.lower().replace(" ", "_")
    literals.add(cons_str)
    return Clause(literals)

def fact_to_cnf(fact_key: str, fact_val: Any) -> Clause:
    """Converts a fact into a unit clause."""
    if isinstance(fact_val, bool):
        val_str = "true" if fact_val else "false"
    else:
        val_str = str(fact_val).lower()
    return Clause({f"{fact_key}={val_str}"})
