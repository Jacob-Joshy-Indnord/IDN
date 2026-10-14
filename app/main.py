from datetime import datetime

from fastapi import Cookie, Depends, FastAPI, Header
from pydantic import BaseModel

from .auth import get_current_user_id
from .sessions import InMemorySessionStore, hash_refresh_token

app = FastAPI(title="IDN")

_store = InMemorySessionStore()


def get_session_store() -> InMemorySessionStore:
    return _store


class SessionOut(BaseModel):
    id: str
    device_label: str
    ip: str
    created_at: datetime
    last_used_at: datetime
    is_current: bool


class SessionList(BaseModel):
    sessions: list[SessionOut]


@app.get("/users/me/sessions", response_model=SessionList)
def list_my_sessions(
    user_id: str = Depends(get_current_user_id),
    store: InMemorySessionStore = Depends(get_session_store),
    x_refresh_token: str | None = Header(default=None),
    refresh_token: str | None = Cookie(default=None),
) -> SessionList:
    """List the caller's active sessions.

    The current session is the one whose refresh token the caller presents
    (``X-Refresh-Token`` header, else ``refresh_token`` cookie).
    """
    presented = x_refresh_token or refresh_token
    current_hash = hash_refresh_token(presented) if presented else None
    return SessionList(
        sessions=[
            SessionOut(
                id=s.id,
                device_label=s.device_label,
                ip=s.ip,
                created_at=s.created_at,
                last_used_at=s.last_used_at,
                is_current=s.refresh_token_hash == current_hash,
            )
            for s in store.list_active_for_user(user_id)
        ]
    )
