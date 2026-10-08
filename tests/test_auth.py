from datetime import timedelta

import jwt
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app

client = TestClient(app)

VALID_CREDENTIALS = {"username": "demo@example.com", "password": "correct horse battery staple"}


def test_sign_in_returns_access_token():
    response = client.post("/auth/sign-in", json=VALID_CREDENTIALS)

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_access_token_expires_in_15_minutes():
    response = client.post("/auth/sign-in", json=VALID_CREDENTIALS)
    body = response.json()

    assert body["expires_in"] == timedelta(minutes=15).total_seconds()

    decoded = jwt.decode(
        body["access_token"],
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
    lifetime = decoded["exp"] - decoded["iat"]
    assert lifetime == timedelta(minutes=15).total_seconds()


def test_sign_in_rejects_invalid_credentials():
    response = client.post(
        "/auth/sign-in",
        json={"username": "demo@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
