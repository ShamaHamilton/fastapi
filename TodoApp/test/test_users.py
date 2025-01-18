from fastapi import Response, status

from .utils import *
from ..routers.users import get_db, get_current_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response: Response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'testusertest'
    assert response.json()['email'] == 'testusertest@mail.com'
    assert response.json()['first_name'] == 'User'
    assert response.json()['last_name'] == 'Test'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(111)-111-11-11'


def test_change_password_success(test_user):
    response: Response = client.put(
        '/user/password',
        json={'password': 'testpassword', 'new_password': 'newpassword'}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response: Response = client.put(
        '/user/password',
        json={'password': 'wrong_password', 'new_password': 'newpassword'}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change.'}


def test_change_phone_number_success(test_user):
    response: Response = client.put('/user/phonenumber/2222222222')
    assert response.status_code == status.HTTP_204_NO_CONTENT
