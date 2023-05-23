from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_listEvents():
    response = client.get("/?skip=0&limit=10")
   
    assert response.status_code == 200
   
    data = response.json()
   
    assert isinstance(data, list)
    for event in data:
        assert "id" in event
        assert "name" in event
        assert "venue" in event
        assert "date" in event
        assert "price" in event
        assert "profile" in event



def test_findEventsByAdmin():
    # Assuming userId = 1
    response = client.get("/app?skip=0&limit=10", headers={"Authorization": "Bearer your_access_token"})

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    for event in data:
        assert "id" in event
        assert "name" in event
        assert "venue" in event
        assert "date" in event
        assert "price" in event
        assert "img" in event
        assert "isEnabled" in event
        assert "tickettypes" in event




def test_findEventById_existing_event():
    # Assuming id = 1 for an existing event
    response = client.get("/1")
  
    assert response.status_code == 200
  
    data = response.json()
  
    assert "name" in data
    assert "description" in data
    assert "venue" in data
    assert "date" in data
    assert "cover" in data
    assert "tickets" in data
    assert "organizer" in data



def test_findEventById_nonexistent_event():
    # Assuming id = 999 for a nonexistent event
    response = client.get("/999")
  
    assert response.status_code == 400
  
    error = response.json()
  
    assert "detail" in error
    assert error["detail"] == "Event not found."




def test_createEvent_success():
    # Assuming a valid AdminEvent payload
    event_payload = {
        "name": "Test Event",
        "description": "This is a test event",
        "venue": "Test Venue",
        "date": "2023-01-01",
        "time": "12:00:00",
        "ticketTypes": [
            {
                "name": "General Admission",
                "price": 10.0,
                "quantity": 100
            }
        ]
    }

    response = client.post("/", json=event_payload)
  
    assert response.status_code == 200
  
    data = response.json()
  
    assert "success" in data
    assert "message" in data
    assert data["success"] is True
    assert data["message"] == "Event created."




def test_createEvent_missing_admin():
    # Assuming an AdminEvent payload with missing admin
    event_payload = {
        "name": "Test Event",
        "description": "This is a test event",
        "venue": "Test Venue",
        "date": "2023-01-01",
        "time": "12:00:00",
        "ticketTypes": [
            {
                "name": "General Admission",
                "price": 10.0,
                "quantity": 100
            }
        ]
    }

    response = client.post("/", json=event_payload)
  
    assert response.status_code == 200
  
    data = response.json()
  
    assert "success" in data
    assert "message" in data
    assert data["success"] is True
    assert data["message"] == "Event created."




def test_createEvent_invalid_payload():
    # Assuming an invalid payload with missing required fields
    invalid_payload = {}

    response = client.post("/", json=invalid_payload)
   
    assert response.status_code == 422
