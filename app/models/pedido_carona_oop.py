from pydantic import BaseModel
from datetime import datetime
from app.models.user_oop import UserModel

class PedidoCaronaBase(BaseModel):
    fk_user: int
    hora_partida_minima: datetime
    hora_partida_maxima: datetime
    valor: float
    local_partida: str
    local_chegada: str

class PedidoCaronaCreate(PedidoCaronaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
    

class PedidoCaronaUpdate(BaseModel):
    hora_partida_minima: datetime | None = None
    hora_partida_maxima: datetime | None = None
    valor: float | None = None

class PedidoCaronaExtended(PedidoCaronaCreate):
    user: UserModel
    