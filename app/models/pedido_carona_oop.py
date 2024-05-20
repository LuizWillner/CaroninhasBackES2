from pydantic import BaseModel
from datetime import datetime
from app.models.user_oop import UserModel

class PedidoCaronaBase(BaseModel):
    fk_user: int
    hora_partida_minima: datetime
    hora_partida_maxima: datetime
    coord_partida: str
    coord_destino: str

class PedidoCaronaCreate(PedidoCaronaBase):
    created_at: datetime

class PedidoCaronaUpdate(PedidoCaronaBase):
    pass

class PedidoCaronaExtended(PedidoCaronaBase):
    id: int
    created_at: datetime
    user: UserModel

    class Config:
        orm_mode = True
    
    