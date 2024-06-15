from pydantic import BaseModel
from datetime import datetime


class AvaliacaoMotorista(BaseModel):
    nota_motorista: int
    comentario_motorista: str
    
class AvaliacaoPassageiro(BaseModel):
    nota_passageiro: int
    comentario_passageiro: str
    
class AvaliacaoResponse(BaseModel):
    id: int
    nota_media: float | None = None
    