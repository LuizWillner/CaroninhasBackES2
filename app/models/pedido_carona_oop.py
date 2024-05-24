from pydantic import BaseModel
from datetime import datetime
from app.models.user_oop import UserModel


class PedidoCaronaBasePartidaDestino(BaseModel):
    local_partida: str
    local_destino: str

class PedidoCaronaBase(PedidoCaronaBasePartidaDestino):
    fk_user: int
    hora_partida_minima: datetime
    hora_partida_maxima: datetime
    valor: float

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
    local_partida: str | None = None
    local_destino: str | None = None

class PedidoCaronaExtended(PedidoCaronaCreate):
    user: UserModel
    