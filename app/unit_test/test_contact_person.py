from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_registerContactPerson_success():
    # Assuming a valid ContactPerson payload
    contact_person_payload = {
        "name": "Ahmed Mahmoud",
        "email": "ahmed@example.com",
        "phone": "1234567890"
    }

    response = client.post("/", json=contact_person_payload)
   
    assert response.status_code == 200
   
    data = response.json()
   
    assert "success" in data
    assert "message" in data
    assert data["success"] is True
    assert data["message"] == "Contact person registered."




def test_registerContactPerson_invalid_payload():
    # Assuming an invalid payload with missing required fields
    invalid_payload = {}

    response = client.post("/", json=invalid_payload)
   
    assert response.status_code == 422






def test_listContactPersons():
    # Assuming some existing contact persons in the database
    response = client.get("/")
  
    assert response.status_code == 200
  
    data = response.json()
  
    assert isinstance(data, list)
    # Assuming at least one contact person is returned
    assert len(data) >= 1

    for person in data:
        assert "name" in person
        assert "email" in person
        assert "phone" in person
        




def test_listContactPersons_pagination():
    # Assuming some existing contact persons in the database
    skip = 0
    limit = 5

    response = client.get(f"/?skip={skip}&limit={limit}")
 
    assert response.status_code == 200
 
    data = response.json()
 
    assert isinstance(data, list)
    assert len(data) <= limit




def test_getContactPersonById_success():
    # Assuming a valid contact person ID
    contact_person_id = 1

    response = client.get(f"/{contact_person_id}")
  
    assert response.status_code == 200
  
    data = response.json()
  
    assert isinstance(data, dict)
    assert "id" in data
    assert data["id"] == contact_person_id




def test_getContactPersonById_not_found():
    # Assuming a non-existent contact person ID
    invalid_contact_person_id = 999

    response = client.get(f"/{invalid_contact_person_id}")
  
    assert response.status_code == 200
  
    data = response.json()
  
    assert isinstance(data, dict)
    assert len(data) == 0
