import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated
from fastapi import Depends, HTTPException, status

from app.utils.db_utils import get_db

from app.database.carona_orm import Carona
from app.database.user_orm import User, Motorista
from app.database.veiculo_orm import MotoristaVeiculo

from app.models.carona_oop import CaronaBase, CaronaExtended, CaronaUpdate

from app.core.motorista import get_current_active_motorista
from app.core.authentication import (
    get_current_active_user
)


def add_carona_to_db(
    carona_to_add: CaronaBase,
    db: Annotated[Session, Depends(get_db)]
) -> Carona:
    db_carona = Carona(
        fk_motorista = carona_to_add.fk_motorista,
        fk_motorista_veiculo = carona_to_add.fk_motorista_veiculo,
        hora_partida = carona_to_add.hora_partida,
        valor=carona_to_add.valor
    )
    try:
        db.add(db_carona)
        db.commit()
    except SQLAlchemyError as sqlae:
        msg = f"Não foi possível adicionar a carona ao banco: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    
    return db_carona


def get_carona_by_id(
    carona_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> Carona:
    carona = db.query(Carona).filter(Carona.id == carona_id).first()
    if not carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Carona id={carona_id} não encontrada.")
    return carona


def update_carona_in_db(
    db_carona: Carona,
    carona_new_info: CaronaUpdate,
    db: Annotated[Session, Depends(get_db)]
) -> Carona:
    if carona_new_info.fk_motorista_veiculo is not None:
        db_carona.fk_motorista_veiculo = carona_new_info.fk_motorista_veiculo
    if carona_new_info.hora_partida is not None:
        db_carona.hora_partida = carona_new_info.hora_partida
    if carona_new_info.valor is not None:
        db_carona.valor = carona_new_info.valor
    
    try:
        db.add(db_carona)
        db.commit()
    except SQLAlchemyError as sqlae:
        msg = f"Não foi possível atualizar a carona no banco: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    
    return db_carona


def remove_carona_from_db(
    db_carona: Carona,
    db: Annotated[Session, Depends(get_db)]
) -> Carona:
    
    try:
        db.delete(db_carona)
        db.commit()
    except SQLAlchemyError as sqlae:
        msg = f"Não foi possível deletar a carona do banco: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    
    return db_carona
