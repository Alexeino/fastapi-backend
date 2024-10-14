from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from .schema import UserRegisterationRequest, UserResponse, Token
from db.session import LOCAL_SESSION
from typing import Annotated
from sqlalchemy.orm import Session
from .models import UserManager
import logging
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from .utils import authenticate_user, jwt_auth

user_router = APIRouter(prefix="/user", tags=["User Management"])


def get_db():
    db = LOCAL_SESSION()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@user_router.post("/register", response_model=UserResponse)
async def register_user(user: UserRegisterationRequest, db: db_dependency):
    try:
        user = UserManager.create_user(user, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logging.info(msg=f"User {user.username} created succesfully!")
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@user_router.post("/token/", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    token = authenticate_user(form_data.username, form_data.password, db)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return {"access_token": token, "token_type": "Bearer"}


@user_router.get("/protected")
async def protected_route(user: Annotated[dict, Depends(jwt_auth)]):
    return {"user": user}
