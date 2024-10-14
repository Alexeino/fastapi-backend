from .models import UserManager, User
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from settings.config import settings
from typing import Annotated
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "role": role}

    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not UserManager.verify_password(password, user.hashed_password):
        return False

    token = create_access_token(
        user.username, user.id, user.role.value, timedelta(minutes=30)
    )
    return token


async def jwt_auth(
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/user/token"))]
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username = payload.get("sub")
        user_id = payload.get("id")
        user_role = payload.get("role")

        if not username and not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"username": username, "user_id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
