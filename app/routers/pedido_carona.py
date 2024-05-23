from app.database.user_orm import User
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Annotated
from sqlalchemy.orm import Session
from app.database.pedido_carona_orm import PedidoCarona
from pydantic import BaseModel

from datetime import datetime
from app.models.pedido_carona_oop import PedidoCaronaBase, PedidoCaronaCreate, PedidoCaronaUpdate, PedidoCaronaExtended
from app.utils.db_utils import get_db
from app.core.pedido_carona import (
    add_pedido_carona_to_db, 
    get_pedido_carona_by_id, 
    get_pedido_caronas, 
    update_pedido_carona_in_db, 
    delete_pedido_carona_from_db
)
from app.core.authentication import get_current_active_user
from app.models.router_tags import RouterTags


router = APIRouter(prefix="/pedido_carona", tags=[RouterTags.pedido_carona])


@router.post("", response_model=PedidoCaronaExtended)
def create_pedido_carona(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    hora_partida_minima: datetime = Query(datetime.now()),
    hora_partida_maxima: datetime = Query(),
    valor_sugerido: float = Query()
    # coord_partida: str,
    # coord_destino: str,
) -> PedidoCaronaExtended:
    pedido_carona = add_pedido_carona_to_db(
        pedido_carona_to_add=PedidoCaronaBase(
            fk_user=current_user.id,
            hora_partida_maxima=hora_partida_maxima,
            hora_partida_minima=hora_partida_minima,
            valor=valor_sugerido,
            # coord_partida=coord_partida,
            # coord_destino=coord_destino
        ),
        db=db
    )
    return pedido_carona


@router.get("/{pedido_carona_id}", response_model=PedidoCaronaExtended)
def read_pedido_carona(
    pedido_carona_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)]  # precisa estar logado para usar o endpoint
) -> PedidoCaronaExtended:
    pedido_carona = get_pedido_carona_by_id(db, pedido_carona_id)
    if not pedido_carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PedidoCarona not found.")
    return pedido_carona


@router.get("/", response_model=List[PedidoCaronaExtended])
def read_pedido_caronas(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0, 
    limit: int = 10
) -> List[PedidoCaronaExtended]:
    return get_pedido_caronas(db, skip=skip, limit=limit)


@router.put("/{pedido_carona_id}", response_model=PedidoCaronaExtended)
def update_pedido_carona(
    pedido_carona_id: int,
    pedido_carona: PedidoCaronaUpdate,
    db: Annotated[Session, Depends(get_db)]
) -> PedidoCaronaExtended:
    return update_pedido_carona_in_db(db=db, pedido_carona_id=pedido_carona_id, pedido_carona=pedido_carona)


class DeletePedidoCaronaResponse(BaseModel):
    message: str


@router.delete("/{pedido_carona_id}", response_model=DeletePedidoCaronaResponse)
def delete_pedido_carona(
    pedido_carona_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> PedidoCaronaExtended:
    return delete_pedido_carona_from_db(db=db, pedido_carona_id=pedido_carona_id)


@router.get("", response_model=list[PedidoCaronaExtended])
def search_caronas(
    hora_minima: datetime = Query(None, description="Hora mínima de partida da carona"),
    hora_maxima: datetime = Query(None, description="Hora máxima de partida da carona"),
    coord_partida: str = Query(None, description="Coordenada de partida da carona"),
    coord_destino: str = Query(None, description="Coordenada de destino da carona"),
    db: Session = Depends(get_db)
) -> list[PedidoCaronaExtended]:
    filters = []
    if hora_minima == None:
        hora_minima = '1900-01-01 00:00:00.000000'
    if hora_maxima == None:
        hora_maxima = '2100-01-01 00:00:00.000000'

    if hora_minima:
        filters.append(PedidoCarona.hora_partida_minima >= hora_minima)
    if hora_maxima:
        filters.append(PedidoCarona.hora_partida_maxima <= hora_maxima)

    filters.append(PedidoCarona.coord_partida  == coord_partida)
    
    filters.append(PedidoCarona.coord_destino == coord_destino)

    caronas = db.query(PedidoCarona).filter(*filters).all()
    return caronas
