import logging

from typing import Annotated
from datetime import timedelta

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.database.user_orm import User

from app.models.general_oop import BasicResponse
from app.models.token_oop import TokenModel
from app.models.router_tags import RouterTags
from app.models.user_oop import UserCreate, UserModel

from app.utils.db_utils import get_db
from app.core.authentication import (
    ACCESS_TOKEN_EXPIRE_DAYS, change_current_user_info, get_active_user, get_current_active_user, authenticate_user, 
    create_access_token, get_user_by_email, add_user_to_db
)


router = APIRouter(tags=[RouterTags.authentication])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=TokenModel)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> TokenModel:
    
    user: User = authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db,
    )
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


@router.post("/users/create", response_model=UserModel)
def create_user(
    db: Annotated[Session, Depends(get_db)],
    user_to_create: UserCreate,
) -> UserModel:
    
    db_user = get_user_by_email(db=db, email=user_to_create.email)
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail already registered."
        )
    
    db_user = add_user_to_db(db=db, user_to_add=user_to_create)
    
    return db_user


@router.get("/users/me", response_model=UserModel)
def read_my_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> UserModel:
    
    return current_user


@router.get("/users/{id}", response_model=UserModel)
def read_user(
    user: Annotated[User, Depends(get_active_user)],
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> UserModel:
    
    return user


@router.patch("/users/me", response_model=BasicResponse)
def update_my_user(
    updated_user: Annotated[User, Depends(change_current_user_info)]
)-> BasicResponse:
    '''
    Atualiza primeiro nome, último nome, data de nascimento 
    '''
    if updated_user:
        return BasicResponse(
            response="User updated."
        )
