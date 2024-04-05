from pydantic import BaseModel
from datetime import datetime


class UserModel(BaseModel):
    email: str
    first_name: str
    last_name: str
    cpf: str
    active: bool
    
class UserWithPassword(UserModel):
    password: str | None = None

class UserExtended(UserModel):
    birthdate: datetime
    created_at: datetime
    iduff: str | None = None
    
class UserWithId(UserExtended):
    id: int
