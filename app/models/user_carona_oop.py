from pydantic import BaseModel
from datetime import datetime
from app.models.user_oop import MotoristaWithUser, UserWithoutMotorista
from app.models.veiculo_oop import MotoristaVeiculoModel

class UserCaronaBase(BaseModel):
    fk_user: int
    fk_carona: int

# class UserCaronaCreate(UserCaronaBase):
#     created_at: datetime

class UserCaronaUpdate(UserCaronaBase):
    pass

class UserCaronaWithUser(UserCaronaBase):
    id: int
    created_at: datetime
    user: UserWithoutMotorista
    class Config:
        orm_mode = True
         
class CaronaSecondary(BaseModel):  # Modelo de Carona criado para evitar circular import caso importasse o modelo de carona_oop.py
    id: int
    created_at: datetime
    updated_at: datetime
    hora_partida: datetime
    valor: float
    motorista: MotoristaWithUser
    veiculo_do_motorista: MotoristaVeiculoModel

class UserCaronaExtended(UserCaronaBase):
    carona: CaronaSecondary
