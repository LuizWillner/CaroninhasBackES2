from pydantic import BaseModel
from datetime import datetime
from app.models.veiculo_oop import MotoristaVeiculoModel
# from app.models.carona_oop import CaronaModel


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    cpf: str
    birthdate: datetime
    iduff: str | None = None
    phone: str
    
class UserCreate(UserBase):
    password: str
    
class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    birthdate: datetime | None = None
    old_password: str | None = None
    new_password: str | None = None

# ===========================================================================    

class MotoristaBase(BaseModel):
    id_fk_user: int
    num_cnh: str
    
class MotoristaModel(MotoristaBase):
    created_at: datetime
    class Config:
        orm_mode = True

class MotoristaWithVeiculos(MotoristaModel):
    motorista_veiculo: list[MotoristaVeiculoModel] = []

class MotoristaWithUser(MotoristaModel):
    user: UserBase

# ===========================================================================   

class UserWithoutMotorista(UserBase):
    id: int
    active: bool = True
    created_at: datetime
    class Config:
        orm_mode = True

class UserModel(UserWithoutMotorista):
    motorista: MotoristaModel | None = None
        