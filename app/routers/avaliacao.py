from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.core.motorista import get_current_active_motorista
from app.utils.db_utils import get_db
from app.core.authentication import get_current_active_user
from app.database.user_carona_orm import UserCarona
from app.database.carona_orm import Carona

from app.models.user_carona_oop import UserCaronaModel, UserCaronaWithUser
from app.models.avaliacao_opp import AvaliacaoMotorista, AvaliacaoPassageiro


from app.models.router_tags import RouterTags
from app.database.user_orm import Motorista, User


router = APIRouter(prefix="/avaliacao", tags=[RouterTags.avaliacao])


@router.post("/passageiro",response_model=UserCaronaModel, description="Notas de 1 a 5 para avaliação", 
             response_model_exclude=["nota_motorista", "comentário_sobre_motorista"])
def avaliar_passageiro(
    db: Annotated[Session, Depends(get_db)],
    current_motorista: Annotated[Motorista, Depends(get_current_active_motorista)],
    carona_id: int,
    user_avaliado_id: int,
    avaliacao: AvaliacaoPassageiro
) -> UserCaronaModel:
    if avaliacao.nota_passageiro > 5 or avaliacao.nota_passageiro < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Valor da avaliação deve ser entre 1 e 5")

    carona = db.query(Carona).filter(Carona.id == carona_id, Carona.fk_motorista == current_motorista.id_fk_user).first()
    if not carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carona não encontrada.")
    
    user_carona = db.query(UserCarona).filter(UserCarona.fk_carona == carona.id, UserCarona.fk_user == user_avaliado_id).first()
    if not user_carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado na carona.")
    elif user_carona.nota_passageiro or user_carona.comentário_sobre_passageiro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Avaliação já foi feita.")
    
    user_carona.nota_passageiro = avaliacao.nota_passageiro
    user_carona.comentário_sobre_passageiro = avaliacao.comentario_passageiro
    
    try:
        db.add(user_carona)
        db.commit()
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro ao criar avaliação sobre passageiro id={user_avaliado_id}")
    
    return user_carona


@router.post("/motorista",response_model=UserCaronaModel, description="Notas de 1 a 5 para avaliação", 
             response_model_exclude=["nota_pasageiro", "comentário_sobre_passageiro"])
def avaliar_motorista(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    carona_id: int,
    motorista_avaliado_id: int,
    avaliacao: AvaliacaoMotorista
) -> UserCaronaModel:
    if avaliacao.nota_motorista > 5 or avaliacao.nota_motorista < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Valor da avaliação deve ser entre 1 e 5")
    
    user_carona: UserCarona = db.query(UserCarona).filter(UserCarona.fk_carona == carona_id, UserCarona.fk_user == current_user.id).first()
    if not user_carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado na carona.")
    
    if user_carona.carona.fk_motorista != motorista_avaliado_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Motorista não encontrado na carona.")
    elif user_carona.nota_motorista or user_carona.comentário_sobre_motorista:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Avaliação já foi feita.")
    
    user_carona.nota_motorista = avaliacao.nota_motorista
    user_carona.comentário_sobre_motorista = avaliacao.comentario_motorista
    
    try:
        db.add(user_carona)
        db.commit()
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro ao criar avaliação sobre motorista id={motorista_avaliado_id}")
    
    return user_carona
