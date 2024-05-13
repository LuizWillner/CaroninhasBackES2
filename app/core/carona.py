import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated
from fastapi import Depends, HTTPException, status

from app.core.db_utils import get_db

from app.database.carona_orm import Carona
from app.database.user_orm import User, Motorista
from app.database.veiculo_orm import MotoristaVeiculo

from app.models.carona_oop import CaronaBase

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
        logging.error(f"Could not add user to database: {sqlae}")
        raise sqlae
    
    return db_carona