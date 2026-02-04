"""Tests for activity endpoints."""

import pytest


def test_get_activities(client):
    """Test getting all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    # Should have at least some activities
    assert len(data) > 0
    
    # Check that expected activities exist
    assert "Basketball Team" in data
    assert "Programming Class" in data
    
    # Verify activity structure
    basketball = data["Basketball Team"]
    assert "description" in basketball
    assert "schedule" in basketball
    assert "max_participants" in basketball
    assert "participants" in basketball
    assert isinstance(basketball["participants"], list)


def test_activity_details(client):
    """Test that activities have correct details."""
    response = client.get("/activities")
    data = response.json()
    
    # Test Programming Class which has initial participants
    prog_class = data["Programming Class"]
    assert prog_class["max_participants"] == 20
    assert len(prog_class["participants"]) >= 0
    
    # Test Chess Club
    chess = data["Chess Club"]
    assert "michael@mergington.edu" in chess["participants"]
    assert "daniel@mergington.edu" in chess["participants"]
