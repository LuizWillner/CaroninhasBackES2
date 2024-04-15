import os
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv

from app.core.db_utils import get_db

from app.database.user_orm import User

from app.models.user_oop import UserCreate
from app.models.token_oop import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv(dotenv_path="credentials.env")

SECRET_KEY = os.environ.get("HASH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1


def add_user_to_db(db: Session, user_to_add: UserCreate) -> User:
    db_user = User(
        email=user_to_add.email,
        first_name=user_to_add.first_name,
        last_name=user_to_add.last_name,
        cpf=user_to_add.cpf,
        birthdate=user_to_add.birthdate,
        iduff=user_to_add.iduff,
        hashed_password=get_password_hash(user_to_add.password),
    )
    
    try:
        db.add(db_user)
        db.commit()
    except SQLAlchemyError as sqlae:
        logging.error(f"Could not add user to database: {sqlae}")
        raise sqlae
    
    return db_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
        
        
def get_user_by_email(db: Session, email: str) -> User | None:
    user_db = db.query(User).filter(User.email == email).first()
    return user_db

        
def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_email(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user_db = get_user_by_email(db=db, email=token_data.username) 
     
    if user_db is None:
        raise credentials_exception
    
    return user_db


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
