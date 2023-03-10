import pytest
from app import client


def test_index():
    response = client.get('/')
    assert response.status_code == 200
    
def test_login():
    response = client.get('/auth/login')
    assert response.status_code == 200

def test_valid_auth():
    data={"login": "silwar",
          "password" : "admin"}
    response = client.post('/auth/login', data=data)
    assert response.status_code == 302

def test_invalid_auth():
    data={"login": "silwar",
          "password" : "user"}
    response = client.post('/auth/login', data=data)
    assert response.status_code == 200

def test_logout():
    response=client.get('/auth/logout')
    assert response.status_code==302
    
