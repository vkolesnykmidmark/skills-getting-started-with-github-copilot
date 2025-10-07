import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)

def test_signup_and_delete_participant():
    # Use a test email and activity
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Ensure not already signed up
    client.delete(f"/activities/{activity}/participant", params={"email": email})

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Check participant is in list
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

    # Delete participant
    response = client.delete(f"/activities/{activity}/participant", params={"email": email})
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

    # Check participant is removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
