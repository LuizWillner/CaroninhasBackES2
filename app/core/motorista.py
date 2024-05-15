import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated
from fastapi import Depends, HTTPException, status

from app.utils.db_utils import get_db

from app.database.user_orm import User, Motorista
from app.database.veiculo_orm import MotoristaVeiculo

from app.models.user_oop import MotoristaBase

from app.core.authentication import (
    get_current_active_user
)


def add_motorista_to_db(
    motorista: MotoristaBase,
    db: Annotated[Session, Depends(get_db)]
) -> Motorista:
    
    db_motorista = (
        db.query(Motorista).
        filter(Motorista.id_fk_user == motorista.id_fk_user)
        .first()
    )
    if db_motorista:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já é motorista"
        )
    
    db_motorista = Motorista(
        id_fk_user = motorista.id_fk_user,
        num_cnh = motorista.num_cnh
    )
    try:
        db.add(db_motorista)
        db.commit()
    except SQLAlchemyError as sqlae:
        msg = f"Não foi possível adicionar o motorista ao banco: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    return db_motorista


def get_current_active_motorista(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
) -> Motorista:
    motorista: Motorista = (
        db.query(Motorista)
        .filter(Motorista.id_fk_user == current_user.id)
        .first()
    )
    if not motorista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not a driver.")
    
    return motorista

