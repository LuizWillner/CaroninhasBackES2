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

from app.models.user_oop import UserCreate, UserUpdate
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
        phone=user_to_add.phone
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


def get_user_by_id(id: int, db: Session) -> User | None:
    user_db: User = db.query(User).filter(User.id == id).first()
    return user_db
        
        
def get_user_by_email(email: str, db: Session) -> User | None:
    user_db = db.query(User).filter(User.email == email).first()
    return user_db

        
def authenticate_user(username: str, password: str, db: Session) -> User | None:
    user = get_user_by_email(email=username, db=db)
    if not user:
        return None
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
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


def get_user(
    id: int,
    db: Annotated[Session, Depends(get_db)]
) -> User:
    
    user = get_user_by_id(id=id, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return user


def get_active_user(
    user: Annotated[User, Depends(get_user)]
) -> User:
    
    if not user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


def change_user_first_name(user: User, new_first_name: str) -> User:
    if new_first_name is not None and user.first_name != new_first_name:
        user.first_name = new_first_name
    return user


def change_user_last_name(user: User, new_last_name: str) -> User:
    if new_last_name is not None and user.last_name != new_last_name:
        user.last_name = new_last_name
    return user


def change_user_birthdate(user: User, new_birthdate: datetime) -> User:
    if new_birthdate is not None and user.birthdate != new_birthdate:
        user.birthdate = new_birthdate
    return user


def change_user_password(user: User, new_password: str, old_password: str) -> User:
    if new_password is not None and old_password is not None:
        if not verify_password(plain_password=old_password, hashed_password=user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password."
            )
        elif not verify_password(plain_password=new_password, hashed_password=user.hashed_password):
            user.hashed_password = get_password_hash(new_password)
    return user


def change_current_user_info(
    user_to_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    
    current_user = change_user_first_name(user=current_user, new_first_name=user_to_update.first_name)
    current_user = change_user_last_name(user=current_user, new_last_name=user_to_update.last_name)
    current_user = change_user_birthdate(user=current_user, new_birthdate=user_to_update.birthdate)
    current_user = change_user_password(
        user=current_user,
        new_password=user_to_update.new_password,
        old_password=user_to_update.old_password
    )
    
    try:
        db.add(current_user)
        db.commit()
    except SQLAlchemyError as sqlae:
        logging.error(f"Could not update user in database: {sqlae}")
        raise sqlae
    
    return current_user
