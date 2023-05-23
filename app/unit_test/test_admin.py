from main import app
from fastapi.testclient import TestClient
from models.user import User, ModelUser
from fastapi_sqlalchemy import db


def test_adminendPoint_getAdminEvent():
    # Initiate a client using app
    client = TestClient(app)

    # Initiate a test event using event id and user id
    test_event_id = 11
    test_user_id = 11

    # Make a GET request to the '/event/{id}' endpoint with the test event ID and user ID
    response = client.get(f'/event/{test_event_id}?userId={test_user_id}')

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Converst the response to a JSON obj
    response_json = response.json()

    # check that the response JSON contains the expected fields
    assert "name" in response_json
    assert "venue" in response_json
    assert "date" in response_json
    assert "description" in response_json
    assert "cover" in response_json
    assert "attendees" in response_json
    assert "tickettypes" in response_json


def test_adminendPoint_getEventStatistics():
    # Initiate a client using app
    client = TestClient(app)

    # Create a test event
    event_id = 11

    # Make a GET request to the endpoint
    response = client.get(
        f"/event/statistics/{event_id}", headers={"Authorization": "Bearer {token}"})

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response JSON contains the expected keys or values
    data = response.json()
    assert "name" in data
    assert "cover" in data
    assert "date" in data
    assert "time" in data
    assert "description" in data
    assert "venue" in data
    assert "organizer" in data
    assert "counters" in data
    assert "genderPercentage" in data
    assert "ticketsData" in data
    assert "ticketTypes" in data
    assert "attendees" in data


def test_adminendPoint_putevent():
    # Initiate a client using app
    client = TestClient(app)

    # Create a test event
    event_id = 11

    # Define the updated event data
    updated_event_data = {
        "name": "ShEvent",
        "profile": "profile",
        "capacity": 10,
        "date": "2023-06-01",
        "time": "18:00:00",
        "description": "description",
        "venue": "Updated venue",
        "ticketTypes": [
            {
                "id": 10,
                "name": "General",
                "price": 10.0,
                "limit": 100,
                "seated": False,
                "seats": None  # Not sure
            },
            {
                "id": 10,
                "name": "VIP",
                "price": 50.0,
                "limit": 50,
                "seated": True,
                "seats": 100  # Not sure
            }
        ]
    }

    # Make a request to the endpoint
    response = client.put(
        f"/event/{event_id}", json=updated_event_data, headers={"Authorization": "Bearer {token}"})

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response JSON contains the expected keys and values
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Event updated."
