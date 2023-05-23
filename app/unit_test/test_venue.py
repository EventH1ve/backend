from fastapi.testclient import TestClient
from main import app
from fastapi_sqlalchemy import db
from models.venue import Venue as ModelVenue, VenueRestriction, VenueContact as ModelVenueContact, ContactPerson as ModelContactPerson
from schemas.venue import Venue, VenueRestriction, VenueContact, ContactPerson


client = TestClient(app)


def test_listVenues():
    # Assuming some existing venues in the database
    response = client.get("/")
   
    assert response.status_code == 200
   
    data = response.json()
   
    assert isinstance(data, list)

    for item in data:
        assert isinstance(item, dict)
        assert "id"in item
        assert "name"in item
        assert "capacity"in item
        assert "description" in item
        assert "createdby" in item
        assert "buildingnumber" in item
        assert "streetname" in item
        assert "city" in item
        assert "country" in item



def test_createVenue():
    venue_data = {
        # dummy data example
        "id": 1,
        "name": "city hall",
        "capacity": 100,
        "description": "test venue",
        "createdby": "ahmad mahmoud",
        "buildingnumber": 3,
        "streetname": "street",
        "city": "Cairo",
        "country": "Egypt"
    }

    response = client.post("/", json=venue_data)
   
    assert response.status_code == 200
   
    data = response.json()
   
    assert "success" in data
    assert "message" in data

    assert data["success"] is True
    assert data["message"] == "Venue created."

    # Query the database to check if the venue was created
    venue = db.session.query(ModelVenue).filter(
        ModelVenue.name == venue_data["name"]).first()
    
    assert venue is not None
    assert venue.name == venue_data["name"]
    db.session.delete(venue)
    db.session.commit()




def test_findVenue():
    # Create a test venue in the database
    test_venue = ModelVenue(name="Test Venue",
        id= 37,
        streetname="123 Test St",
        city="Test City",
        country="Test Country",
        capacity = 100,
        description = "test venue",
        createdby = "ahmad mahmoud",
        buildingnumber = 3,)
    
    db.session.add(test_venue)
    db.session.commit()

    # Send a GET request to find the test venue
    response = client.get(f"/{test_venue.id}")
   
    assert response.status_code == 200
   
    data = response.json()
   
    assert data == test_venue.dict()



def test_addVenueRestriction(tet_client):
    # Create a test venue restriction
    test_restriction = VenueRestriction(restriction_type="Test Restriction", details="Test details")

    # Send a POST request to add the venue restriction
    response = client.post("/venue/restriction", json=test_restriction.dict())
   
    assert response.status_code == 200
   
    data = response.json()
   
    assert data == {"success": True, "message": "Venue restriction added."}




def test_getVenueRestrictions():
    # Create a test venue ID
    test_venue_id = 1

    # Send a GET request to retrieve the venue restrictions
    response = client.get(f"/restriction/{test_venue_id}")
   
    assert response.status_code == 200
   
    data = response.json()
   
    assert isinstance(data, list)  # Verify that the response is a list
    # Add more assertions to verify the structure and content of the response data as per your requirements




def test_addVenueContact():
    # Create a test venue contact object
    test_venue_contact = {
        "id": 1,
        "venueid": 1,
        "contactid": 2,
    }

    # Send a POST request to add the venue contact
    response = client.post("/contact", json=test_venue_contact)
   
    assert response.status_code == 200
   
    data = response.json()
   
    assert data["success"] is True
    assert data["message"] == "Venue contact information added."
    # Add more assertions or queries to verify the addition of the venue contact in the database






def test_getVenueContacts():
    # Create a test venue ID
    test_venue_id = 1

    # Send a GET request to retrieve venue contacts
    response = client.get(f"/contact/{test_venue_id}")

    assert response.status_code == 200

    data = response.json()

    # Perform assertions to verify the response data
    assert isinstance(data, list)
    # Add more assertions or queries to verify the venue contacts retrieved from the database

