"""Access-token authentication (stand-in until the token-issuance task lands)."""
import os

import jwt
from fastapi import Header, HTTPException

JWT_SECRET = os.environ.get("IDN_JWT_SECRET", "dev-secret")
JWT_ALGORITHM = "HS256"


def get_current_user_id(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        claims = jwt.decode(
            authorization[7:], JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    sub = claims.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token")
    return sub
