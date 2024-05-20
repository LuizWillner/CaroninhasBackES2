from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.carona_orm import Carona
from app.database.user_orm import Motorista
from app.database.veiculo_orm import MotoristaVeiculo

from app.models.carona_oop import CaronaBase, CaronaExtended

from app.utils.db_utils import get_db
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

@router.get("", response_model=list[CaronaExtended])
def search_caronas(
    hora_minima: datetime = Query(None, description="Hora mínima de partida da carona"),
    hora_maxima: datetime = Query(None, description="Hora máxima de partida da carona"),
    valor_minimo: float = Query(None, description="Valor mínimo da carona"),
    valor_maximo: float = Query(None, description="Valor máximo da carona"),
    db: Session = Depends(get_db)
) -> list[CaronaExtended]:
    filters = []
    if valor_minimo == None:
        valor_minimo = 0
    if valor_maximo == None:
        valor_maximo = 999999
    if hora_minima == None:
        hora_minima = '1900-01-01 00:00:00.000000'
    if hora_maxima == None:
        hora_maxima = '2100-01-01 00:00:00.000000'

    if hora_minima:
        filters.append(Carona.hora_partida >= hora_minima)
    if hora_maxima:
        filters.append(Carona.hora_partida <= hora_maxima)
    if valor_minimo:
        filters.append(Carona.valor >= valor_minimo)
    if valor_maximo:
        filters.append(Carona.valor <= valor_maximo)

    caronas = db.query(Carona).filter(*filters).all()
    return caronas