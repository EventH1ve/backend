from main import app
from fastapi.testclient import TestClient
from models.user import User, ModelUser
from fastapi_sqlalchemy import db
from schemas.ticket import TicketType, TicketValidity, TicketInfo


def test_verify_ticket_validity():
    # Initiate a client using app
    client = TestClient(app)

    # Simulate an authenticated admin user
    admin_user_id = 1

    # Create a valid ticket info object
    ticket_info = {
        "ticketId": "123",
        "gate": "Gate A",
        "eventId": 456
    }

    # Send a POST request to the endpoint
    response = client.post("/verify", json=ticket_info,
                           headers={"user-id": str(admin_user_id)})

    # Check the response status code and data
    assert response.status_code == 200
    assert response.json() == {"valid": True}


def test_verify_ticket_validity_non_admin():
    # Initiate a client using app
    client = TestClient(app)

    # Simulate a non-admin user
    non_admin_user_id = 2

    # Create a valid ticket info object
    ticket_info = {
        "ticketId": "123",
        "gate": "Gate A",
        "eventId": 456
    }

    # Send a POST request to the endpoint
    response = client.post("/verify", json=ticket_info,
                           headers={"user-id": str(non_admin_user_id)})

    # Check the response status code and data
    assert response.status_code == 403
    assert response.json() == {"detail": "User is not an Admin."}


def test_verify_ticket_validity_already_checked_in():
    # Initiate a client using app
    client = TestClient(app)

    # Simulate an authenticated admin user
    admin_user_id = 1

    # Create a ticket info object for an already checked-in ticket
    ticket_info = {
        "ticketId": "122",
        "gate": "Gate A",
        "eventId": 456
    }

    # Send a POST request to the endpoint
    response = client.post("/verify", json=ticket_info,
                           headers={"user-id": str(admin_user_id)})

    # Check the response status code and data
    assert response.status_code == 200
    assert response.json() == {"valid": False}


def test_create_ticket():
    # Initiate a client using app
    client = TestClient(app)

    # Create a ticket type object
    ticket_type = {
        "name": "General Admission",
        "price": 20.0,
        "limit": 100,
        "seated": False,
        "seats": None,
        "eventid": 123
    }

    # Send a POST request to the endpoint
    response = client.post("/type", json=ticket_type)

    # Check the response status code and data
    assert response.status_code == 200
    assert response.json() == {"success": True,
                               "message": "Ticket type created."}


def test_list_ticket_types():
    # Initiate a client using app
    client = TestClient(app)

    # Add some ticket types to the database for testing
    # Asumming that there is no tickets yet
    ticket_type1 = {
        "name": "General",
        "price": 20.0,
        "limit": 100,
        "seated": False,
        "seats": None,
        "eventid": 123
    }
    ticket_type2 = {
        "name": "VIP",
        "price": 2.0,
        "limit": 10,
        "seated": False,
        "seats": None,
        "eventid": 125
    }

    db.session.add(ticket_type1)
    db.session.add(ticket_type2)
    db.session.commit()

    # Send a GET request to the endpoint
    response = client.get("/type")

    # Check the response status code and data
    assert response.status_code == 200
    ticket_types = response.json()
    assert len(ticket_types) == 2  # Check the number of ticket types returned
    assert ticket_types[0]["name"] == "General"  
    assert ticket_types[1]["name"] == "VIP" 
