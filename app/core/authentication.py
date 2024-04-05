import os

from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv

from app.models.user_oop import UserModel, UserWithPassword
from app.models.token_oop import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv(dotenv_path="credentials.env")

SECRET_KEY = os.environ.get("HASH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str) -> UserModel:
    #TODO: conectar com o banco de verdade
    if username in db:
        user_dict = db[username]
        return UserModel(
            email=user_dict.get("email"),
            first_name=user_dict.get("first_name"),
            last_name=user_dict.get("last_name"),
            cpf=user_dict.get("cpf"),
            active=user_dict.get("active")
        )
        
        
def get_user_with_password(db, username: str) -> UserWithPassword:
    #TODO: conectar com o banco de verdade
    if username in db:
        user_dict = db[username]
        return UserWithPassword(
            email=user_dict.get("email"),
            first_name=user_dict.get("first_name"),
            last_name=user_dict.get("last_name"),
            cpf=user_dict.get("cpf"),
            active=user_dict.get("active"),
            password=user_dict.get("hashed_password")
        )
        
        
def authenticate_user(db, username: str, password: str) -> UserWithPassword:
    user = get_user_with_password(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
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


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserModel:
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
    
    #TODO: conectar com o banco de verdade
    from app.security.authentication import fake_users_db
    user = get_user(fake_users_db, username=token_data.username) 
     
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> UserModel:
    
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
