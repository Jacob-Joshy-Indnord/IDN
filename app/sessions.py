"""Session model and store. Refresh tokens are only ever stored hashed."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Session:
    user_id: str
    refresh_token_hash: str
    device_label: str
    ip: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=_now)
    last_used_at: datetime = field(default_factory=_now)
    revoked_at: datetime | None = None

    @property
    def is_active(self) -> bool:
        return self.revoked_at is None


class InMemorySessionStore:
    """Placeholder for the PostgreSQL-backed store from the sessions-table task."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def create(self, *, created_at: datetime | None = None, **kwargs) -> Session:
        session = Session(**kwargs)
        if created_at:
            session.created_at = session.last_used_at = created_at
        self._sessions[session.id] = session
        return session

    def list_active_for_user(self, user_id: str) -> list[Session]:
        return sorted(
            (s for s in self._sessions.values() if s.user_id == user_id and s.is_active),
            key=lambda s: s.created_at,
        )
