from app.models.carona_oop import CaronaModel
from pydantic import BaseModel
from datetime import datetime
from app.models.user_oop import UserModel

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
    user: UserModel
    carona: CaronaModel

    class Config:
        orm_mode = True
