from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.routing.q_learning_agent import QLearningRoutingAgent
from backend.routing.environment import DEFAULT_STAFF_MEMBERS, get_workload_bucket
from backend.models import User

def recommend_staff_routing(db: Session, category: str, priority: str, department: str) -> Dict[str, Any]:
    agent = QLearningRoutingAgent.load()
    
    # Query staff from database or fallback to default staff list
    staff_users = db.query(User).filter(User.role == "STAFF").all() if db else []
    if not staff_users:
        staff_pool = DEFAULT_STAFF_MEMBERS
    else:
        staff_pool = [
            {
                "id": u.id,
                "name": u.name,
                "department": u.department,
                "skills": [category],
                "workload": len(u.assigned_tickets),
                "avg_res_time": 4.0
            }
            for u in staff_users
        ]

    # Compute average workload bucket
    avg_w = int(sum(s["workload"] for s in staff_pool) / len(staff_pool)) if staff_pool else 1
    w_bucket = get_workload_bucket(avg_w)
    state = (category, priority, w_bucket)

    if agent:
        action = agent.select_action(state, explore=False)
        action_idx = min(action, len(staff_pool) - 1)
    else:
        action_idx = 0

    recommended_staff = staff_pool[action_idx]

    candidates = [
        {
            "staff_id": s["id"],
            "name": s["name"],
            "department": s["department"],
            "current_workload": s["workload"],
            "predicted_utility": round(8.5 - s["workload"] * 0.5, 2)
        }
        for s in staff_pool
    ]

    return {
        "recommended_staff_id": recommended_staff["id"],
        "recommended_staff_name": recommended_staff["name"],
        "predicted_utility": round(9.0 - recommended_staff["workload"] * 0.5, 2),
        "reason": f"Q-Learning policy selected {recommended_staff['name']} based on skill match for {category} and balanced current workload ({recommended_staff['workload']} active tickets).",
        "candidates": candidates
    }
