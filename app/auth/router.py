from fastapi import APIRouter, HTTPException, status

from app.auth.schemas import SignInRequest, TokenResponse
from app.auth.security import create_access_token
from app.auth.users import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-in", response_model=TokenResponse)
def sign_in(payload: SignInRequest) -> TokenResponse:
    user_id = authenticate_user(payload.username, payload.password)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token, issued_at, expires_at = create_access_token(subject=user_id)
    expires_in = int((expires_at - issued_at).total_seconds())

    return TokenResponse(access_token=access_token, expires_in=expires_in)
