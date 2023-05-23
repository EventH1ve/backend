from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_getDashboardMetrics():
   
    # Assuming the necessary environment variables are set
    # Assuming a valid user ID
    user_id = 1

    response = client.get(f"/dashboard?userId={user_id}")
  
    assert response.status_code == 200
  
    data = response.json()
  
    assert "counters" in data
    counters = data["counters"]
   
    assert "upcomingEvents" in counters
    assert "joinedEvents" in counters
    assert "membershipSince" in counters
    assert "upcomingEvents" in data
    assert "history" in data
  
    upcoming_events = data["upcomingEvents"]
    history = data["history"]
  
    assert isinstance(upcoming_events, list)
    assert isinstance(history, list)
    for event in upcoming_events:
        assert "id" in event
        assert "name" in event
        assert "venue" in event
        assert "date" in event
        assert "price" in event
        assert "transactionid" in event
   
    for event in history:
        assert "id" in event
        assert "name" in event
        assert "venue" in event
        assert "date" in event
        assert "price" in event
        assert "transactionid" in event



def test_getAdminDashboardMetrics():
 
    # Assuming the necessary environment variables are set
    # Assuming a valid user ID
    user_id = 1

    response = client.get(f"/dashboard/admin?userId={user_id}")
  
    assert response.status_code == 200
  
    data = response.json()
  
    assert "counters" in data
    counters = data["counters"]
  
    assert "upcomingEvents" in counters
    assert "pastEvents" in counters
    assert "leftDaysforTheMembership" in counters
    assert "upcomingEvents" in data
    assert "pastEvents" in data
  
    upcoming_events = data["upcomingEvents"]
    past_events = data["pastEvents"]
  
    assert isinstance(upcoming_events, list)
    assert isinstance(past_events, list)
    for event in upcoming_events:
        assert "id" in event
        assert "name" in event
        assert "venue" in event
        assert "date" in event
  
    for event in past_events:
        assert "id" in event
        assert "name" in event
        assert "venue" in event
        assert "date" in event
