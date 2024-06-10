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
    db_pedido_carona = PedidoCarona(**pedido_carona_to_add.model_dump())
    
    try:
        db.add(db_pedido_carona)
        db.commit()
    except SQLAlchemyError as sqlae:
        msg = f"Não foi possível adicionar a pedido_carona ao banco: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    
    return db_pedido_carona


def get_pedido_carona_by_id(db: Annotated[Session, Depends(get_db)], pedido_carona_id: int) -> PedidoCarona:
    return db.query(PedidoCarona).filter(PedidoCarona.id == pedido_carona_id).first()


def get_pedido_caronas(db: Session, skip: int = 0, limit: int = 10) -> list[PedidoCarona]:
    return db.query(PedidoCarona).offset(skip).limit(limit).all()


def update_pedido_carona_in_db(db: Session, pedido_carona_id: int, pedido_carona: PedidoCaronaUpdate) -> PedidoCarona:
    db_pedido_carona = get_pedido_carona_by_id(db, pedido_carona_id)
    if not db_pedido_carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido de Carona não encontrado.")
    
    for key, value in pedido_carona.dict().items():
        if value is not None:
            setattr(db_pedido_carona, key, value)
    
    try:
        db.commit()
        db.refresh(db_pedido_carona)
    except SQLAlchemyError as sqlae:
        msg = f"Não foi possível atualizar o Pedido de Carona no banco: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    
    return db_pedido_carona


def update_carona_from_pedido_carona_in_db(db: Session, db_pedido_carona: PedidoCarona, carona_id: int) -> PedidoCarona:
    db_pedido_carona.fk_carona = carona_id
    try:
        db.commit()
        db.refresh(db_pedido_carona)
    except SQLAlchemyError as sqlae:
        msg = f"Não foi possível atrelar o Pedido de Carona a uma Carona no banco: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    
    return db_pedido_carona


def delete_pedido_carona_from_db(db: Session, pedido_carona_id: int) -> str:
    db_pedido_carona = get_pedido_carona_by_id(db, pedido_carona_id)
    if not db_pedido_carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido de Carona não encontrado.")
    
    try:
        db.delete(db_pedido_carona)
        db.commit()
    except SQLAlchemyError as sqlae:
        msg = f"Não foi possível deletar Pedido de Carona do banco: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    return f"Pedido de Carona id={pedido_carona_id} deletado com sucesso!"
