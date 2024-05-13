from pydantic import BaseModel
from datetime import datetime
from app.models.vehicle_oop import MotoristaVeiculoModel


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    cpf: str
    birthdate: datetime
    iduff: str | None = None
    
class UserCreate(UserBase):
    password: str
    
class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    birthdate: datetime | None = None
    old_password: str | None = None
    new_password: str | None = None
    

class MotoristaBase(BaseModel):
    num_cnh: str
    
class MotoristaCreate(MotoristaBase):
    id_fk_user: int
    
class MotoristaModel(MotoristaBase):
    created_at: datetime
    motorista_veiculo: list[MotoristaVeiculoModel] = []
    class Config:
        orm_mode = True
        

class UserModel(UserBase):
    id: int
    active: bool = True
    created_at: datetime
    motorista: MotoristaModel | None = None
    class Config:
        orm_mode = True
        