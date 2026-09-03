import pytest
from fastapi.testclient import TestClient
from backend.app import app
from backend.auth import create_access_token

client = TestClient(app)

def test_tc08_normal_user_attempts_admin_kb_page_http_403():
    """TC08: Normal user attempts admin KB page -> HTTP 403."""
    user_token = create_access_token({"sub": "student@campus.edu", "role": "USER", "id": 8})
    
    response = client.post(
        "/api/knowledge-base/rules",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "rule_id": "R_UNAUTHORIZED",
            "category": "TEST",
            "antecedents": {"test": True},
            "consequent": "Test Fault"
        }
    )
    assert response.status_code == 403
    assert "not authorized" in response.json()["detail"].lower()
