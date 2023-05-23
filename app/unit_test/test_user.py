from main import app
from fastapi.testclient import TestClient
from models.user import User, ModelUser
from fastapi_sqlalchemy import db
import bcrypt


def test_userEndPoint_users():
    client = TestClient(app)
    response = client.get('/')

    # Ensure that the response is 200 OK
    assert response.status_code == 200

    # Converst the response to a JSON obj
    response_json = response.json()

    # Ensure that the response JSON is a list
    assert isinstance(response_json, list)

    # Ensure that all users in the data base hase these fields
    for item in response_json:
        assert isinstance(item, dict)
        assert 'id' in item
        assert 'username' in item
        assert 'email' in item
        assert 'password' in item
        assert 'gender' in item
        assert 'phonenumber' in item
        assert 'firstname' in item
        assert 'lastname' in item
        assert 'type' in item
        assert 'createdat' in item


def test_userendPoint_signup():

    # Create a test client using the FastAPI app
    client = TestClient(app)

    # Define a test user (fake data)
    test_user = {
        "id": "10",
        "username": "password123",
        "email": "shady@gmail.com",
        "password": "shady",
        "gender": "mail",
        "phonenumber": "01023654874",
        "firstname": "shady",
        "lastname": "mohamed",
        "type": "user",
        # "createdat": "admin"
    }
    # Make a POST request the receive the response
    response = client.post('/signup', json=test_user)

    # Ensure that the response is 200 OK
    assert response.status_code == 200

    # Converst the response to a JSON obj
    response_json = response.json()

    # Ensure that these fields are in the response
    assert "success" in response_json
    assert "message" in response_json

    # Ensure that the "sucess" field has a "Trua" value and same as "message"
    assert response_json["success"] is True
    assert response_json["message"] == "User created."

    # Query the database to check if the user was created
    user = db.session.query(ModelUser).filter(
        ModelUser.username == test_user["username"]).first()
    assert user is not None
    assert user.username == test_user["username"]
    db.session.delete(user)
    db.session.commit()


def test_userendPoint_login():
    # Create a test client using the FastAPI app
    client = TestClient(app)

    # Define a test login user (fake data)
    # We assume that this user is not an admin
    test_login_user = {
        "username": "shadyM@gmail.com",
        "password": "13456"
    }

    # Make a POST request to the '/login' endpoint with the test login user data
    response = client.post('/login', json=test_login_user)

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Parse the response content as JSON
    response_json = response.json()

    # Ensure that the response JSON contains the expected fields
    assert "success" in response_json
    assert "message" in response_json
    assert "id" in response_json
    assert "role" in response_json
    assert "username" in response_json
    assert "email" in response_json
    assert "firstName" in response_json
    assert "lastName" in response_json
    assert "mobileNumber" in response_json
    assert "gender" in response_json
    assert "token" in response_json

    # Ensure that the success key is True
    assert response_json["success"] is True

    # Ensure that the message key contains the expected value
    assert response_json["message"] == "Login successful."

    # Perform additional assertions, ...

    # Example: Query the database to check if the user exists and the password is correct
    user = db.session.query(ModelUser).filter(ModelUser.username == test_login_user["username"]).first()

    # Ensure that the user wxist
    assert user is not None
    assert bcrypt.checkpw(test_login_user["password"].encode('utf-8'), user.password.encode('utf-8'))

    # cleanup the session (optional)
    db.session.delete(user)
    db.session.commit()


def test_userendPoint_verifyToken():
    # Create a test client using the FastAPI app
    client = TestClient(app)

    # Define a test token (fake token)
    test_token = "shadyMohamedTestToken"

    # Make a POST request to the '/verifyToken' endpoint with the test token
    response = client.post('/verifyToken', json={"token": test_token})

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Parse the response content as JSON
    response_json = response.json()

    # Ensure that the response JSON contains the expected keys
    assert "success" in response_json
    assert "message" in response_json

    # Ensure that the success key is True
    assert response_json["success"] is True

    # Ensure that the message key contains the expected value
    assert response_json["message"] == "Token validation successful."
