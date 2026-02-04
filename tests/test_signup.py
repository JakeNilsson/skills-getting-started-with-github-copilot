"""Tests for signup functionality."""

import pytest


def test_signup_for_activity(client):
    """Test signing up for an activity."""
    email = "test@mergington.edu"
    activity = "Math Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_signup_duplicate(client):
    """Test that duplicate signups are rejected."""
    email = "emma@mergington.edu"
    activity = "Programming Class"
    
    # Emma is already in Programming Class
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_invalid_activity(client):
    """Test signup for non-existent activity."""
    email = "test@mergington.edu"
    activity = "Nonexistent Activity"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]


def test_signup_persists(client):
    """Test that signup persists in activity list."""
    email = "newstudent@mergington.edu"
    activity = "Debate Team"
    
    # Sign up
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify in activities list
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert email in data[activity]["participants"]
