from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.utils.db_utils import get_db
from app.core.authentication import get_current_active_user
from app.database.user_carona_orm import UserCarona
from app.database.carona_orm import Carona

from app.models.user_carona_oop import UserCaronaWithUser
from app.models.avaliacao_opp import AvaliacaoMotorista, AvaliacaoPassageiro


from app.models.router_tags import RouterTags
from app.database.user_orm import User


router = APIRouter(prefix="/avaliacao", tags=[RouterTags.avaliacao])

@router.post("/motorista",response_model=UserCaronaWithUser, description="Notas de 1 a 5 para avaliação")
def teste_avaliacao_motorista(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    carona_id: int,
    avaliacao: AvaliacaoMotorista
) -> UserCaronaWithUser:
    
    
    db = db
    carona = db.query(Carona).filter(Carona.fk_motorista_veiculo== carona.id, Carona.fk_motorista == current_user.id).first()# faz query da carona passando o id
    user_carona = db.query(UserCarona).filter(UserCarona.fk_carona == carona.id, UserCarona.fk_user == current_user.id).first()
    
    user_carona.nota_motorista = avaliacao.nota_motorista
    user_carona.comentário_sobre_motorista = avaliacao.comentário_motorista
    
    if avaliacao.nota_motorista > 5 or avaliacao.nota_motorista < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Valor deve ser entre 1 e 5")
     
    try:
        db.add(carona)
        db.commit()
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar avaliacao")
    
    try:
        db.add(user_carona)
        db.commit()
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar avaliação")
    
    return user_carona

@router.post("/passageiro",response_model=UserCaronaWithUser, description="Notas de 1 a 5 para avaliação")
def teste_avaliacao_passageiro(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    carona_id: int,
    avaliacao: AvaliacaoPassageiro
) -> UserCaronaWithUser:
    
    db = db
    carona = db.query(Carona).filter(Carona.fk_motorista_veiculo== carona.id, Carona.fk_motorista == current_user.id).first()# faz query da carona passando o id
    user_carona = db.query(UserCarona).filter(UserCarona.fk_carona == carona.id, UserCarona.fk_user == current_user.id).first()
    
    user_carona.nota_motorista = avaliacao.nota_motorista
    user_carona.comentário_sobre_motorista = avaliacao.comentário_motorista
    
    if avaliacao.nota_passageiro > 5 or avaliacao.nota_passageiro < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Valor deve ser entre 1 e 5")
    
    try:
        db.add(carona)
        db.commit()
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar avaliacao")
    
    try:
        db.add(user_carona)
        db.commit()
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar avaliação")
    
    return user_carona