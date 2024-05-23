from pydantic import BaseModel
from datetime import datetime
from app.models.user_carona_oop import UserCaronaWithUser
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
    
class CaronaUpdate(BaseModel):
    fk_motorista_veiculo: int | None = None
    hora_partida: datetime | None = None
    valor: float | None = None

# ===========================================================================

class CaronaExtended(CaronaModel):
    motorista: MotoristaWithUser
    veiculo_do_motorista: MotoristaVeiculoModel
    passageiros: list[UserCaronaWithUser] = []


    
    
    