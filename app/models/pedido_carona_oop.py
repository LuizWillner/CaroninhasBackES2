from pydantic import BaseModel
from datetime import datetime
from app.models.user_oop import UserModel

class PedidoCaronaBase(BaseModel):
    fk_user: int
    hora_partida_minima: datetime
    hora_partida_maxima: datetime
    valor: float
    # coord_partida: str
    # coord_destino: str

class PedidoCaronaCreate(PedidoCaronaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
    

class PedidoCaronaUpdate(PedidoCaronaBase):
    pass

class PedidoCaronaExtended(PedidoCaronaCreate):
    user: UserModel
    