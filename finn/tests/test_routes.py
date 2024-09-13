import pytest
from fastapi import status
from fastapi.testclient import TestClient

from finn.app import app
from finn.schemas.base_schema import Message

HELLO_URL = "/hello"


@pytest.fixture
def client():
    return TestClient(app)


def test_hello(client: TestClient):
    response = client.get(url=HELLO_URL)
    message_schema = Message.model_validate({"message": "hello world!"}).model_dump()
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == message_schema
