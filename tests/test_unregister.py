"""Tests for unregister functionality."""

import pytest


def test_unregister_from_activity(client):
    """Test unregistering from an activity."""
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Verify student is registered
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]
    
    # Unregister
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert email in data["message"]


def test_unregister_persists(client):
    """Test that unregister persists in activity list."""
    email = "daniel@mergington.edu"
    activity = "Chess Club"
    
    # Verify student is registered
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]
    
    # Unregister
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify not in activities list
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]


def test_unregister_not_registered(client):
    """Test unregistering someone not registered."""
    email = "notregistered@mergington.edu"
    activity = "Math Club"
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_invalid_activity(client):
    """Test unregister from non-existent activity."""
    email = "test@mergington.edu"
    activity = "Nonexistent Activity"
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]
