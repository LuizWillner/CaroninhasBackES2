from pydantic import BaseModel
from datetime import datetime


class VeiculoBase(BaseModel):
    tipo: str
    marca: str
    modelo: str
    cor: str | None = None
    
class VeiculoModel(VeiculoBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True
        
# ===========================================================================

class MotoristaVeiculoModel(BaseModel):
    placa: str
    created_at: datetime
    veiculo: VeiculoModel
    class Config:
        orm_mode = True