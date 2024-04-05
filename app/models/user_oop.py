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
    
    
class DriverBase(BaseModel):
    license: str
    
class DriverCreate(DriverBase):
    fk_user: int
    
class DriverModel(BaseModel):
    id: int
    created_at: datetime
    user: UserModel
    driver_vehicle: list[DriverVehicleModel] = []
    class Config:
        orm_mode = True
