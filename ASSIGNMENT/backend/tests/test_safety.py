import pytest
from fastapi.testclient import TestClient
from backend.app import app
from backend.auth import create_access_token

client = TestClient(app)

def test_tc10_out_of_scope_chatbot_question_safe_fallback():
    """TC10: Out-of-scope chatbot question -> safe fallback."""
    token = create_access_token({"sub": "student@campus.edu", "role": "USER", "id": 8})

    res = client.post(
        "/api/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={"message": "What is the capital of France?", "session_id": "test_tc10"}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["intent"] == "unknown"
    assert body["next_action"] == "general"
    assert "Intelligent Campus Helpdesk Assistant" in body["reply"]
