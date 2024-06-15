from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session
from sqlalchemy import exc, func

from app.core.motorista import get_current_active_motorista, get_motorista_by_id
from app.utils.db_utils import get_db
from app.core.authentication import get_current_active_user, get_user_by_id
from app.database.user_carona_orm import UserCarona
from app.database.carona_orm import Carona

from app.models.user_carona_oop import UserCaronaModel, UserCaronaWithUser
from app.models.avaliacao_opp import AvaliacaoMotorista, AvaliacaoPassageiro, AvaliacaoResponse


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


@router.get("/motorista/{motorista_id}", response_model=AvaliacaoResponse, description="Média da avaliação de motorista")
def get_media_avaliacao_motorista(
    motorista: Annotated[Motorista, Depends(get_motorista_by_id)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
)-> AvaliacaoResponse:
    if not motorista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motorista não encontrado.")
    
    nota_media = (
        db.query(func.avg(UserCarona.nota_motorista))
        .join(Carona, Carona.id == UserCarona.fk_carona)
        .filter(Carona.fk_motorista == motorista.id_fk_user)
        .scalar()
    )
    return AvaliacaoResponse(
        id=motorista.id_fk_user,
        nota_media=nota_media
    )


@router.get("/passageiro/{user_id}", response_model=AvaliacaoResponse, description="Média da avaliação de passageiro")
def get_media_avaliacao_passageiro(
    user: Annotated[User, Depends(get_user_by_id)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
)-> AvaliacaoResponse:
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    
    nota_media = (
        db.query(func.avg(UserCarona.nota_passageiro))
        .filter(UserCarona.fk_user == user.id)
        .scalar()
    )
    return AvaliacaoResponse(
        id=user.id,
        nota_media=nota_media
    )