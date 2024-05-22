import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated
from fastapi import Depends, HTTPException, status

from app.utils.db_utils import get_db

from app.database.user_orm import User, Motorista
from app.database.veiculo_orm import MotoristaVeiculo, Veiculo

from app.models.veiculo_oop import MotoristaVeiculoBase, MotoristaVeiculoModel, MotoristaVeiculoUpdate, VeiculoBase, VeiculoModel

from app.core.motorista import get_current_active_motorista
from app.core.authentication import (
    get_current_active_user
)


def add_veiculo_to_db(
    veiculo_to_create: VeiculoBase,
    db: Annotated[Session, Depends(get_db)]
)-> Veiculo:
    
    db_veiculo = Veiculo(
        tipo=veiculo_to_create.tipo.upper(),
        marca=veiculo_to_create.marca.upper(),
        modelo=veiculo_to_create.modelo.upper(),
        cor=veiculo_to_create.cor.upper(),
    )
    try:
        db.add(db_veiculo)
        db.commit()
    except SQLAlchemyError as sqlae:
        msg = f"Não foi possível adicionar o veículo ao banco: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    return db_veiculo


def get_veiculo_by_info(
    tipo: str,
    marca: str,
    modelo: str,
    cor: str,
    db: Annotated[Session, Depends(get_db)]
) -> Veiculo | None:
    db_veiculo = (
        db.query(Veiculo)
        .filter(
            Veiculo.tipo==tipo,
            Veiculo.marca==marca,
            Veiculo.modelo==modelo,
            Veiculo.cor==cor
        )
        .first()
    )
    return db_veiculo


def add_motorista_veiculo_to_db(
    motorista_veiculo_to_create: MotoristaVeiculoBase,
    db: Annotated[Session, Depends(get_db)]
) -> MotoristaVeiculo:
    db_motorista_veiculo = MotoristaVeiculo(
        fk_motorista = motorista_veiculo_to_create.fk_motorista,
        fk_veiculo = motorista_veiculo_to_create.fk_veiculo,
        placa = motorista_veiculo_to_create.placa.upper()
    )
    try:
        db.add(db_motorista_veiculo)
        db.commit()
    except SQLAlchemyError as sqlae:
        msg = f"Não foi possível atribuir veiculo ao motorista no banco: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    
    return db_motorista_veiculo


def get_motorista_veiculo_of_user(
    veiculo_id: int,
    motorista: Annotated[Motorista, Depends(get_current_active_motorista)],
    db: Annotated[Session, Depends(get_db)]
) -> MotoristaVeiculo:
    db_motorista_veiculo: MotoristaVeiculo = (
        db.query(MotoristaVeiculo)
        .filter(
            MotoristaVeiculo.fk_motorista == motorista.id_fk_user,
            MotoristaVeiculo.fk_veiculo == veiculo_id,
            MotoristaVeiculo.active == True
        )
        .first()
    )
    
    return db_motorista_veiculo

def get_motorista_veiculo_of_user_by_placa(
    placa: str,
    motorista: Annotated[Motorista, Depends(get_current_active_motorista)],
    db: Annotated[Session, Depends(get_db)]
) -> MotoristaVeiculo:
    db_motorista_veiculo: MotoristaVeiculo = (
        db.query(MotoristaVeiculo)
        .filter(
            MotoristaVeiculo.fk_motorista == motorista.id_fk_user,
            MotoristaVeiculo.placa == placa,
            MotoristaVeiculo.active == True
        )
        .first()
    )
    return db_motorista_veiculo


def get_all_motorista_veiculo_of_user(
    motorista: Annotated[Motorista, Depends(get_current_active_motorista)],
    db: Annotated[Session, Depends(get_db)]
)-> list[MotoristaVeiculo]:
    db_motorista_veiculo: list[MotoristaVeiculo] = (
        db.query(MotoristaVeiculo)
        .filter(
            MotoristaVeiculo.fk_motorista == motorista.id_fk_user,
            MotoristaVeiculo.active == True
        )
        .all()
    )
    return db_motorista_veiculo


def update_motorista_veiculo_in_db(
    db_motorista_veiculo: Annotated[MotoristaVeiculo, Depends(get_motorista_veiculo_of_user_by_placa)],
    db: Annotated[Session, Depends(get_db)],
    new_placa: str | None = None,
    new_fk_veiculo: int | None = None,
    new_active: bool | None = None
) -> MotoristaVeiculo:
    if new_fk_veiculo is not None:
        db_motorista_veiculo.fk_veiculo = new_fk_veiculo
    if new_placa is not None:
        db_motorista_veiculo.placa = new_placa.upper()
    if new_active is not None:
        db_motorista_veiculo.active = new_active
    
    try:
        db.add(db_motorista_veiculo)
        db.commit()
    except SQLAlchemyError as sqlae:
        msg = f"Não foi possível atualizar o veículo do motorista no banco: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    
    return db_motorista_veiculo
