from fastapi.testclient import TestClient
from fastapi import Response, status

# from .. import main
from ..main import app


client = TestClient(app)


def test_return_health_check():
    response: Response = client.get('/healthy')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}
