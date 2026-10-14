from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi.testclient import TestClient

from app.auth import JWT_ALGORITHM, JWT_SECRET
from app.main import app, get_session_store
from app.sessions import InMemorySessionStore, hash_refresh_token

NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def bearer(user_id: str) -> dict:
    token = jwt.encode({"sub": user_id}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def store():
    s = InMemorySessionStore()
    app.dependency_overrides[get_session_store] = lambda: s
    yield s
    app.dependency_overrides.clear()


@pytest.fixture
def client(store):
    return TestClient(app)


def add(store, user, rt, device, ip, minutes=0, revoked=False):
    s = store.create(
        user_id=user,
        refresh_token_hash=hash_refresh_token(rt),
        device_label=device,
        ip=ip,
        created_at=NOW + timedelta(minutes=minutes),
    )
    s.last_used_at = NOW + timedelta(minutes=minutes + 5)
    if revoked:
        s.revoked_at = NOW
    return s


def test_requires_auth(client):
    assert client.get("/users/me/sessions").status_code == 401


def test_lists_fields_and_marks_current_via_header(client, store):
    a = add(store, "u1", "rt-a", "Chrome on Mac", "1.1.1.1", 0)
    b = add(store, "u1", "rt-b", "iPhone", "2.2.2.2", 10)
    r = client.get(
        "/users/me/sessions", headers={**bearer("u1"), "X-Refresh-Token": "rt-b"}
    )
    assert r.status_code == 200
    items = {i["id"]: i for i in r.json()["sessions"]}
    assert set(items) == {a.id, b.id}
    assert items[b.id]["is_current"] is True
    assert items[a.id]["is_current"] is False
    assert items[b.id]["device_label"] == "iPhone"
    assert items[b.id]["ip"] == "2.2.2.2"
    assert items[b.id]["created_at"].startswith("2026-01-01T00:10")
    assert items[b.id]["last_used_at"].startswith("2026-01-01T00:15")
    assert "refresh_token_hash" not in items[b.id]


def test_marks_current_via_cookie(client, store):
    a = add(store, "u1", "rt-a", "d", "1.1.1.1")
    client.cookies.set("refresh_token", "rt-a")
    r = client.get("/users/me/sessions", headers=bearer("u1"))
    assert r.json()["sessions"][0]["id"] == a.id
    assert r.json()["sessions"][0]["is_current"] is True


def test_no_refresh_token_marks_none(client, store):
    add(store, "u1", "rt-a", "d", "1.1.1.1")
    r = client.get("/users/me/sessions", headers=bearer("u1"))
    assert [s["is_current"] for s in r.json()["sessions"]] == [False]


def test_only_own_and_active_sessions(client, store):
    mine = add(store, "u1", "rt-a", "d", "1.1.1.1")
    add(store, "u1", "rt-old", "old", "1.1.1.1", revoked=True)
    add(store, "u2", "rt-x", "other", "3.3.3.3")
    r = client.get("/users/me/sessions", headers=bearer("u1"))
    assert [s["id"] for s in r.json()["sessions"]] == [mine.id]


def test_other_users_refresh_token_never_marks_current(client, store):
    add(store, "u1", "rt-a", "d", "1.1.1.1")
    add(store, "u2", "rt-x", "other", "3.3.3.3")
    r = client.get(
        "/users/me/sessions", headers={**bearer("u1"), "X-Refresh-Token": "rt-x"}
    )
    assert [s["is_current"] for s in r.json()["sessions"]] == [False]
