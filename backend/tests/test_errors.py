from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.core.errors import NotFoundError, register_error_handlers


class Item(BaseModel):
    name: str


def make_client() -> TestClient:
    app = FastAPI()
    register_error_handlers(app)

    @app.get("/missing")
    def missing():
        raise NotFoundError()

    @app.get("/boom")
    def boom():
        raise RuntimeError("secret internal detail")

    @app.post("/items")
    def items(item: Item):
        return item

    return TestClient(app, raise_server_exceptions=False)


def test_app_error_returns_clean_json():
    response = make_client().get("/missing")
    assert response.status_code == 404
    assert response.json() == {"error": {"code": "not_found", "message": "Not found."}}


def test_unexpected_error_hides_details():
    response = make_client().get("/boom")
    assert response.status_code == 500
    assert "secret internal detail" not in response.text


def test_validation_error_does_not_echo_input():
    response = make_client().post("/items", json={"wrong": "my-password-123"})
    assert response.status_code == 422
    assert "my-password-123" not in response.text

    