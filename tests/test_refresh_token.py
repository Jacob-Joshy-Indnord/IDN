import base64

from app.tokens import REFRESH_TOKEN_BYTES, generate_refresh_token


def _decode(token: str) -> bytes:
    return base64.urlsafe_b64decode(token + "=" * (-len(token) % 4))


def test_refresh_token_encodes_at_least_256_bits():
    token = generate_refresh_token()
    assert isinstance(token, str)
    assert len(_decode(token)) * 8 >= 256
    assert REFRESH_TOKEN_BYTES * 8 >= 256


def test_refresh_token_is_url_safe_and_opaque():
    token = generate_refresh_token()
    assert all(c.isalnum() or c in "-_" for c in token)


def test_refresh_tokens_are_unique():
    assert len({generate_refresh_token() for _ in range(1000)}) == 1000


def test_uses_secrets_source(monkeypatch):
    calls = []

    def fake(n):
        calls.append(n)
        return b"\x01" * n

    monkeypatch.setattr("app.tokens.secrets.token_bytes", fake)
    generate_refresh_token()
    assert calls == [REFRESH_TOKEN_BYTES]
