from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends, HTTPException, status

from app.core.db_utils import get_db

from app.database.user_orm import User, Motorista
from app.database.veiculo_orm import MotoristaVeiculo

from app.core.motorista import get_current_active_motorista
from app.core.authentication import (
    get_current_active_user
)


def get_veiculo_motorista_by_id(
    veiculo_id: int,
    current_motorista: Annotated[Motorista, Depends(get_current_active_motorista)],
    db: Annotated[Session, Depends(get_db)]
) -> MotoristaVeiculo:
    motorista_veiculo: MotoristaVeiculo = (
        db.query(MotoristaVeiculo)
        .filter(
            MotoristaVeiculo.fk_motorista == current_motorista.id_fk_user,
            MotoristaVeiculo.fk_veiculo == veiculo_id
        )
        .first()
    )
    
    return motorista_veiculo


def get_all_veiculo_motorista_of_user(
    current_motorista: Annotated[Motorista, Depends(get_current_active_motorista)],
    db: Annotated[Session, Depends(get_db)]
)-> list[MotoristaVeiculo]:
    motorista_veiculo: list[MotoristaVeiculo] = (
        db.query(MotoristaVeiculo)
        .filter(
            MotoristaVeiculo.fk_motorista == current_motorista.id_fk_user,
        )
        .all()
    )
    return motorista_veiculo