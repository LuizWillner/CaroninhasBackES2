from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Annotated, Optional

from app.core.motorista import get_current_active_motorista
from app.database.veiculo_orm import MotoristaVeiculo
from app.models.user_oop import UserModel
from app.utils.veiculo_utils import TipoVeiculo, MarcaVeiculo, Cor

from app.database.user_orm import Motorista, User

from app.models.router_tags import RouterTags
from app.models.veiculo_oop import MotoristaVeiculoBase, MotoristaVeiculoExtended, MotoristaVeiculoModel, VeiculoBase, VeiculoModel

from app.utils.db_utils import get_db
from app.core.veiculo import add_motorista_veiculo_to_db, add_veiculo_to_db, get_all_motorista_veiculo_of_user, get_motorista_veiculo_of_user_by_placa, get_veiculo_by_info, get_motorista_veiculo_of_user
from app.core.authentication import get_current_active_user


router = APIRouter(prefix="/veiculo", tags=[RouterTags.motorista_e_veiculos])


@router.post("", response_model=VeiculoModel)
def create_veiculo(
    tipo: TipoVeiculo,
    marca: MarcaVeiculo,
    modelo: str,
    cor: Cor,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
) -> VeiculoModel:
    
    veiculo_to_create = VeiculoBase(
        tipo=tipo.value,
        marca=marca.value,
        modelo=modelo,
        cor=cor.value
    )
    
    db_veiculo = get_veiculo_by_info(
        tipo=veiculo_to_create.tipo,
        marca=veiculo_to_create.marca,
        modelo=veiculo_to_create.modelo,
        cor=veiculo_to_create.cor,
        db=db
    )
    if db_veiculo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Veículo já existe."
        )
        
    db_veiculo = add_veiculo_to_db(
        veiculo_to_create=VeiculoBase(
            tipo=tipo.value,
            marca=marca.value,
            modelo=modelo,
            cor=cor.value
        ),
        db=db
    )
    return db_veiculo


@router.post("/me", response_model=UserModel)
def add_veiculo_to_me(
    tipo: TipoVeiculo,
    marca: MarcaVeiculo,
    modelo: str,
    cor: Cor,
    placa: str,
    current_motorista: Annotated[Motorista, Depends(get_current_active_motorista)],
    curent_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
) -> UserModel:
    veiculo = VeiculoBase(
        tipo=tipo.value,
        marca=marca.value,
        modelo=modelo,
        cor=cor.value
    )
    
    db_veiculo = get_veiculo_by_info(
        tipo=veiculo.tipo,
        marca=veiculo.marca,
        modelo=veiculo.modelo,
        cor=veiculo.cor,
        db=db
    )
    if not db_veiculo:
        db_veiculo = add_veiculo_to_db(veiculo_to_create=veiculo, db=db)
    
    db_veiculo_motorista = get_motorista_veiculo_of_user(veiculo_id=db_veiculo.id, motorista=current_motorista, db=db)
    if db_veiculo_motorista:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Motorista já possui o veículo {veiculo.marca} {veiculo.modelo} {veiculo.cor}."
        )
    
    db_veiculo_motorista = add_motorista_veiculo_to_db(
        motorista_veiculo_to_create=MotoristaVeiculoBase(
            fk_motorista=current_motorista.id_fk_user,
            fk_veiculo=db_veiculo.id,
            placa=placa
        ),
        db=db
    )
    
    return curent_user


@router.get("/me", response_model=MotoristaVeiculoExtended)
def read_my_veiculo_by_placa(
    db_motorista_veiculo: Annotated[MotoristaVeiculo, Depends(get_motorista_veiculo_of_user_by_placa)],
    placa: str
) -> MotoristaVeiculoExtended:
    '''
    - Procura pelo veículo de placa {_placa_} do usuário atual
    - Retorna informações do veículo
    '''
    if not db_motorista_veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhum veículo com placa {placa} encontrado para o usuário."
        )
    return db_motorista_veiculo


@router.get("/me/all", response_model=list[MotoristaVeiculoExtended])
def read_all_my_veiculos(
    all_motorista_veiculo: Annotated[list[MotoristaVeiculo], Depends(get_all_motorista_veiculo_of_user)],
) -> list[MotoristaVeiculoExtended]:
    '''
    - Procura por todos os veículos do usuário atual
    - Retorna informações dos veículos
    '''
    return all_motorista_veiculo
