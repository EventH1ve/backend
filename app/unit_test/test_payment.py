from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_createPaymentEntry_success():
    # Assuming the necessary environment variables are set
    payment_info = {
        "orderId": "123456",
        "eventId": 1,
        "subtotal": 50,
        "tickets": [
            {
                "ticket_type": "General",
                "count": 2,
                "seats": [1, 2]
            }
        ]
    }

    response = client.post("/", json=payment_info)
  
    assert response.status_code == 200
  
    data = response.json()
  
    assert "qrURL" in data
    assert isinstance(data["qrURL"], list)
    assert len(data["qrURL"]) == 2  # Assuming 2 tickets were created



def test_createPaymentEntry_existing_transaction():
    # Assuming the necessary environment variables are set
    # Assuming there is an existing entry with the same transaction ID
    payment_info = {
        "orderId": "existing_order_id",
        "eventId": 1,
        "subtotal": 50,
        "tickets": [
            {
                "ticket_type": "General",
                "count": 2,
                "seats": [1, 2]
            }
        ]
    }

    response = client.post("/", json=payment_info)
  
    assert response.status_code == 400
  
    data = response.json()
  
    assert "detail" in data
    assert data["detail"] == "Transaction already recorded."



def test_getUserPaidEvents():
  
    # Assuming the necessary environment variables are set
    # Assuming a valid user ID
    user_id = 1

    response = client.get(f"/user?userId={user_id}")
  
    assert response.status_code == 200
  
    data = response.json()
  
    assert isinstance(data, list)
    for item in data:
        assert "id" in item
        assert "userid" in item
        assert "eventid" in item
        assert "price" in item
        assert "transactionid" in item
        assert "tickettype" in item
