from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.token_oop import TokenModel
from app.models.user_oop import UserBase, UserCreate
from app.models.router_tags import RouterTags
from app.core.authentication import (
    ACCESS_TOKEN_EXPIRE_DAYS, get_current_active_user, authenticate_user, 
    create_access_token
)


router = APIRouter(tags=[RouterTags.authentication])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johndoe@example.com": {
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "cpf": "123.456.789-10",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$SWRstZpgNoDupJVUasc/3uEYjUO5GolRDKigrqNRIAK2ubwboM17S",
        "active": True,
    },
    "alice@example.com": {
        "username": "alice",
        "cpf": "000.000.000-00",
        "first_name": "Alice",
        "last_name": "Wonderson",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$e1GbE2BT64udPZmGnwQ/GebfO9Z5FUpc3v8aKP2hJY/WqkhEONgTO",
        "active": False,
    },
}


@router.post("/token", response_model=TokenModel)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenModel:
    user: UserCreate = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return TokenModel(access_token=access_token, token_type="bearer")


@router.get("/users/me", response_model=UserBase)
def read_users_me(current_user: Annotated[UserBase, Depends(get_current_active_user)]) -> UserBase:
    return current_user
