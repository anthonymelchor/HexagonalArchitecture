import uuid
import requests

ENDPOINT = "http://127.0.0.1:5000"

def test_can_create_user():
    
    payload_login = {
        "email": "melchor@gmail.com",
        "password": "1234"
    }

    response_login = login(payload_login)
    assert response_login.status_code == 200

    data_login = response_login.json()

    headers = {
        "Authorization": f"{data_login['access_token']}"
    }

    email = create_random_email()

    payload_user = {
        "name":"user_test",
        "role":"customer",
        "email":email,
        "password":"password_test",
        "avatar":"avatar_test"
    }
    
    response_user = create_user(payload_user, headers)
    assert response_user.status_code == 200

    data_user = response_user.json()
    response_get_user = get_user(data_user["id"], headers)

    assert response_get_user.status_code == 200
    get_user_data = response_get_user.json()

    assert get_user_data["name"] == payload_user["name"]
    assert get_user_data["role"] == payload_user["role"]
    

def login(payload):
    user = requests.post(f"{ENDPOINT}/api/v1/auth/login", json=payload)
    return user

def create_user(payload, header):
    user = requests.post(f"{ENDPOINT}/api/v1/users", json=payload, headers=header)
    return user 

def create_random_email():
    return f"{uuid.uuid4().hex}@gmail.com"

def get_user(id, header):
    user = requests.get(f"{ENDPOINT}/api/v1/users/{id}", headers=header)
    return user