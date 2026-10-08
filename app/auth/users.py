from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Stub user store. Real credential/identity management is out of scope for
# this task; this exists only to give the sign-in endpoint something to
# authenticate against until the real user store lands.
_STUB_USERS = {
    "demo@example.com": {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "password_hash": _pwd_context.hash("correct horse battery staple"),
    }
}


def authenticate_user(username: str, password: str) -> str | None:
    """Return the user id if the credentials are valid, else None."""
    user = _STUB_USERS.get(username)
    if user is None:
        return None
    if not _pwd_context.verify(password, user["password_hash"]):
        return None
    return user["user_id"]
