import pytest
import uuid
from fastapi.testclient import TestClient
from backend.app import app
from backend.auth import create_access_token

client = TestClient(app)

def test_tc09_duplicate_incomplete_report_rejected():
    """TC09: Duplicate/incomplete report -> rejected."""
    token = create_access_token({"sub": "student@campus.edu", "role": "USER", "id": 8})

    # Test 1: Incomplete report (short description)
    res_incomplete = client.post(
        "/api/tickets",
        headers={"Authorization": f"Bearer {token}"},
        json={"department": "CSE", "location": "Room 101", "description": "bad"}
    )
    assert res_incomplete.status_code == 422

    # Test 2: Valid report first time
    unique_desc = f"Unique issue for duplicate test {uuid.uuid4().hex[:6]}"
    unique_loc = f"Lab {uuid.uuid4().hex[:4]}"
    res1 = client.post(
        "/api/tickets",
        headers={"Authorization": f"Bearer {token}"},
        json={"department": "CSE", "location": unique_loc, "description": unique_desc}
    )
    assert res1.status_code == 200

    # Test 3: Duplicate report submission
    res_dup = client.post(
        "/api/tickets",
        headers={"Authorization": f"Bearer {token}"},
        json={"department": "CSE", "location": unique_loc, "description": unique_desc}
    )
    assert res_dup.status_code == 409
    assert "duplicate" in res_dup.json()["detail"].lower()
