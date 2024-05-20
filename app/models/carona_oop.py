from pydantic import BaseModel
from datetime import datetime
from app.models.user_oop import MotoristaWithUser, UserModel
from app.models.veiculo_oop import MotoristaVeiculoModel


class CaronaBase(BaseModel):
    fk_motorista: int
    fk_motorista_veiculo: int
    hora_partida: datetime
    valor: float
    
class CaronaModel(CaronaBase):
    id: int
    created_at: datetime
    updated_at: datetime

# ===========================================================================

class UserCaronaModel(BaseModel):
    id: int
    created_at: datetime
    #updated_at: datetime
    
class UserCaronaWithUser(UserCaronaModel):
    user: UserModel

# ===========================================================================

class CaronaExtended(CaronaModel):
    motorista: MotoristaWithUser
    veiculo_do_motorista: MotoristaVeiculoModel
    passageiros: list[UserCaronaWithUser] = []


    
    
    