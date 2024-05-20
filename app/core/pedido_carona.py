import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from app.utils.db_utils import get_db

from app.database.pedido_carona_orm import PedidoCarona
from app.database.user_orm import User

from app.models.pedido_carona_oop import PedidoCaronaBase, PedidoCaronaUpdate, PedidoCaronaCreate

from app.core.motorista import get_current_active_motorista
from app.core.authentication import (
    get_current_active_user
)

def add_pedido_carona_to_db(
    pedido_carona_to_add: PedidoCaronaBase,
    db: Annotated[Session, Depends(get_db)]
) -> PedidoCarona:
    db_pedido_carona = PedidoCarona(
        hora_partida_minima = pedido_carona_to_add.hora_partida_minima,
        hora_partida_maxima = pedido_carona_to_add.hora_partida_maxima,
        coord_partida = pedido_carona_to_add.coord_partida,
        coord_destino = pedido_carona_to_add.coord_destino,
        fk_user = pedido_carona_to_add.fk_user
    )
    try:
        db.add(db_pedido_carona)
        db.commit()
    except SQLAlchemyError as sqlae:
        msg = f"Não foi possível adicionar a pedido_carona ao banco: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    
    return db_pedido_carona

def get_pedido_carona_by_id(db: Session, pedido_carona_id: int) -> PedidoCarona:
    pedido_carona = db.query(PedidoCarona).filter(PedidoCarona.id == pedido_carona_id).first()
    if not pedido_carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PedidoCarona not found")
    return pedido_carona

def get_pedido_carona_by_id(db: Session, pedido_carona_id: int) -> PedidoCarona:
    return db.query(PedidoCarona).filter(PedidoCarona.id == pedido_carona_id).first()

def get_pedido_caronas(db: Session, skip: int = 0, limit: int = 10) -> list[PedidoCarona]:
    return db.query(PedidoCarona).offset(skip).limit(limit).all()

def update_pedido_carona_in_db(db: Session, pedido_carona_id: int, pedido_carona: PedidoCaronaUpdate) -> PedidoCarona:
    db_pedido_carona = get_pedido_carona_by_id(db, pedido_carona_id)
    if not db_pedido_carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PedidoCarona not found.")
    
    for key, value in pedido_carona.dict().items():
        setattr(db_pedido_carona, key, value)
    
    try:
        db.commit()
        db.refresh(db_pedido_carona)
    except SQLAlchemyError as sqlae:
        msg = f"Could not update PedidoCarona in the database: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    return db_pedido_carona

class SuccessResponse(BaseModel):
    message: str

def delete_pedido_carona_from_db(db: Session, pedido_carona_id: int) -> SuccessResponse:
    db_pedido_carona = get_pedido_carona_by_id(db, pedido_carona_id)
    if not db_pedido_carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PedidoCarona not found.")
    
    try:
        db.delete(db_pedido_carona)
        db.commit()
    except SQLAlchemyError as sqlae:
        msg = f"Could not delete PedidoCarona from the database: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    return SuccessResponse(message="Pedido de Carona deletado com sucesso!")