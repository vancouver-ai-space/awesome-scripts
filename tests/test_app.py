import pytest
from app import app
import json


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """Test that the home route returns the index.html file"""
    response = client.get("/")
    assert response.status_code == 200


def test_chat_route(client):
    """Test the chat endpoint with sample user data"""
    test_data = {
        "message": "How can I improve my well-being?",
        "userInfo": {"age": "30", "location": "New York", "occupation": "Teacher"},
    }

    response = client.post(
        "/chat", data=json.dumps(test_data), content_type="application/json"
    )

    assert response.status_code == 200
    assert "response" in response.json
