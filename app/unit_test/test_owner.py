from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_getOwnerMetrics():
    
    response = client.get("/")
    
    assert response.status_code == 200
    
    response_json = response.json()
    
    assert "counters" in response_json
    assert "organizers" in response_json["counters"]
    assert "attendees" in response_json["counters"]
    assert "totalAccounts" in response_json["counters"]
    assert "activeEvents" in response_json["counters"]
    assert "transactionsProcessed" in response_json["counters"]
    assert "admins" in response_json
    assert isinstance(response_json["admins"], list)



def test_organizerRequest_success():
    request_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password",
        "gender": "male",
        "phonenumber": "1234567890",
        "firstname": "Test",
        "lastname": "User",
        "subscription": 30,
        "logo": "test_logo.png"
    }

    response = client.post("/request", json=request_data)

    assert response.status_code == 200

    data = response.json()

    assert "success" in data
    assert data["success"] is True
    assert "message" in data
    assert data["message"] == "Request placed."




def test_organizerRequest_existing_user():

    # Assuming there is an existing user with the username "existing_user"
    request_data = {
        "username": "existing_user",
        "email": "testuser@example.com",
        "password": "password",
        "gender": "male",
        "phonenumber": "1234567890",
        "firstname": "Test",
        "lastname": "User",
        "subscription": 30,
        "logo": "test_logo.png"
    }

    response = client.post("/request", json=request_data)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "User already exists."



def test_getUnapprovedAdmins():
   
    # Assuming there are unapproved admins in the database
    response = client.get("/unapproved")
 
    assert response.status_code == 200
 
    data = response.json()
 
    assert isinstance(data, list)
    for user in data:
        assert "id" in user
        assert "username" in user
        assert "firstname" in user
        assert "lastname" in user
        assert "email" in user
