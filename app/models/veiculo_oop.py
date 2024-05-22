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

class MotoristaVeiculoBase(BaseModel):
    fk_motorista: int
    fk_veiculo: int
    placa: str

class MotoristaVeiculoModel(BaseModel):
    placa: str
    created_at: datetime
    veiculo: VeiculoModel
    class Config:
        orm_mode = True
        
class MotoristaVeiculoExtended(MotoristaVeiculoModel):
    id: int
    fk_motorista: int
    fk_veiculo: int
    
class MotoristaVeiculoUpdate(BaseModel):
    new_cor: str | None = None
    new_placa: str | None = None