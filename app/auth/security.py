from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings


def create_access_token(subject: str, *, now: datetime | None = None) -> tuple[str, datetime, datetime]:
    """Mint a short-lived JWT access token for ``subject``.

    Returns the encoded token along with its issued-at and expiry timestamps.
    """
    issued_at = now or datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": subject,
        "iat": issued_at,
        "exp": expires_at,
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, issued_at, expires_at
