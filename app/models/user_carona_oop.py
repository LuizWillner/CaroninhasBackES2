from pydantic import BaseModel
from datetime import datetime

class UserCaronaBase(BaseModel):
    fk_user: int
    fk_carona: int

class UserCaronaCreate(UserCaronaBase):
    created_at: datetime

class UserCaronaUpdate(UserCaronaBase):
    pass

class UserCaronaExtended(UserCaronaBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
