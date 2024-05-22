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
from app.models.veiculo_oop import MotoristaVeiculoBase, MotoristaVeiculoExtended, MotoristaVeiculoModel, MotoristaVeiculoUpdate, VeiculoBase, VeiculoModel

from app.utils.db_utils import get_db
from app.core.veiculo import add_motorista_veiculo_to_db, add_veiculo_to_db, get_all_motorista_veiculo_of_user, get_motorista_veiculo_of_user_by_placa, get_veiculo_by_info, get_motorista_veiculo_of_user, update_motorista_veiculo_in_db
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


@router.post("/me", response_model=MotoristaVeiculoExtended)
def add_veiculo_to_me(
    tipo: TipoVeiculo,
    marca: MarcaVeiculo,
    modelo: str,
    cor: Cor,
    placa: str,
    current_motorista: Annotated[Motorista, Depends(get_current_active_motorista)],
    curent_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
) -> MotoristaVeiculoExtended:
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
    
    db_motorista_veiculo = get_motorista_veiculo_of_user(veiculo_id=db_veiculo.id, motorista=current_motorista, db=db)
    if db_motorista_veiculo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Motorista já possui o veículo {veiculo.marca} {veiculo.modelo} {veiculo.cor}."
        )
    
    db_motorista_veiculo = add_motorista_veiculo_to_db(
        motorista_veiculo_to_create=MotoristaVeiculoBase(
            fk_motorista=current_motorista.id_fk_user,
            fk_veiculo=db_veiculo.id,
            placa=placa
        ),
        db=db
    )
    
    return db_motorista_veiculo


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


@router.patch("/me", response_model=MotoristaVeiculoExtended)
def update_my_veiculo(
    motorista_veiculo_update: MotoristaVeiculoUpdate,
    db_motorista_veiculo: Annotated[MotoristaVeiculo, Depends(get_motorista_veiculo_of_user_by_placa)],
    placa: str,
    db: Annotated[Session, Depends(get_db)]
) -> MotoristaVeiculoExtended:
    '''
    - Atualiza informações de um veículo do motorista, passando sua placa no param _placa_. 
    - Podem ser alterados a cor do veículo (_new_cor_ no body) e/ou a placa (_new_placa_ no body). 
    Valores nulos em qualquer um dos campos indicam que a respectiva informação não será atualizada no banco.
    - Retorna a veículo do motorista atualizado
    '''
    
    if not db_motorista_veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhum veículo com placa {placa} encontrado para o usuário."
        )
    
    fk_veiculo = None
    
    if motorista_veiculo_update.new_cor:
        db_veiculo = get_veiculo_by_info(
            tipo=db_motorista_veiculo.veiculo.tipo,
            marca=db_motorista_veiculo.veiculo.marca,
            modelo=db_motorista_veiculo.veiculo.modelo,
            cor=motorista_veiculo_update.new_cor,
            db=db
        )
        if not db_veiculo:
            db_veiculo = add_veiculo_to_db(
                veiculo_to_create=VeiculoBase(
                    tipo=db_motorista_veiculo.veiculo.tipo,
                    marca=db_motorista_veiculo.veiculo.marca,
                    modelo=db_motorista_veiculo.veiculo.modelo,
                    cor=motorista_veiculo_update.new_cor
                ),
                db=db
            )
        fk_veiculo = db_veiculo.id
    
    db_motorista_veiculo = update_motorista_veiculo_in_db(
        db_motorista_veiculo=db_motorista_veiculo,
        db=db,
        new_fk_veiculo=fk_veiculo,
        new_placa=motorista_veiculo_update.new_placa
    )
        
    return db_motorista_veiculo


# @router.delete("/me", response_model=str)
# def delete_my_veiculo_and_caronas() -> str:
#     return