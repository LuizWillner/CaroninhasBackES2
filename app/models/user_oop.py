from pydantic import BaseModel
from datetime import datetime
from app.models.vehicle_oop import DriverVehicleModel


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    cpf: str
    birthdate: datetime
    iduff: str | None = None
    
class UserCreate(UserBase):
    password: str    

class UserModel(UserBase):
    id: int
    active: bool = True
    created_at: datetime
    class Config:
        orm_mode = True
        
class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    birthdate: datetime | None = None
    old_password: str | None = None
    new_password: str | None = None
    
class DriverBase(BaseModel):
    license: str
    
class DriverCreate(DriverBase):
    fk_user: int
    
class DriverModel(DriverBase):
    id: int
    created_at: datetime
    user: UserModel
    driver_vehicle: list[DriverVehicleModel] = []
    class Config:
        orm_mode = True
