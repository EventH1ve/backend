from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_partnerEndPoint_listPartners():

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
        assert 'name' in item
        assert 'img' in item

