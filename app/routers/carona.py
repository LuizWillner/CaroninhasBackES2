from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session

from app.database.user_orm import Motorista
from app.database.veiculo_orm import MotoristaVeiculo

from app.models.carona_oop import CaronaBase, CaronaExtended

from app.core.db_utils import get_db
from app.core.carona import add_carona_to_db
from app.core.motorista import get_current_active_motorista
from app.core.veiculo import get_motorista_veiculo_of_user
from app.models.router_tags import RouterTags


router = APIRouter(prefix="/carona", tags=[RouterTags.carona])


@router.post("", response_model=CaronaExtended)
def create_carona(
    motorista: Annotated[Motorista, Depends(get_current_active_motorista)],
    motorista_veiculo: Annotated[MotoristaVeiculo, Depends(get_motorista_veiculo_of_user)],
    veiculo_id: int,
    hora_de_partida: datetime,
    preco_carona: float,
    db: Annotated[Session, Depends(get_db)]
)-> CaronaExtended:
    if not motorista_veiculo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle of current user with id {veiculo_id} not found.")
    carona = add_carona_to_db(
        carona_to_add=CaronaBase(
            fk_motorista=motorista.id_fk_user,
            fk_motorista_veiculo=motorista_veiculo.id,
            hora_partida= hora_de_partida,
            valor=preco_carona
        ),
        db=db
    )
    return carona