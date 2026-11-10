"""Refresh token generation."""
import base64
import secrets

# 32 bytes = 256 bits of entropy (minimum required by spec).
REFRESH_TOKEN_BYTES = 32


def generate_refresh_token() -> str:
    """Return an opaque, URL-safe refresh token encoding 256 random bits.

    Bytes come from the OS CSPRNG via ``secrets``; the token carries no
    structure or claims.
    """
    raw = secrets.token_bytes(REFRESH_TOKEN_BYTES)
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")
