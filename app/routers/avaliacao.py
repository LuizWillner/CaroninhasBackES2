from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.utils.db_utils import get_db
from app.core.authentication import get_current_active_user
from app.database.user_carona_orm import UserCarona
from app.database.carona_orm import Carona

from app.models.user_carona_oop import UserCaronaModel, UserCaronaWithUser
from app.models.avaliacao_opp import AvaliacaoMotorista, AvaliacaoPassageiro


from app.models.router_tags import RouterTags
from app.database.user_orm import User


router = APIRouter(prefix="/avaliacao", tags=[RouterTags.avaliacao])


@router.post("/passageiro",response_model=UserCaronaModel, description="Notas de 1 a 5 para avaliação")
def avaliacao_passageiro(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    carona_id: int,
    user_avaliado_id: float,
    avaliacao: AvaliacaoPassageiro
) -> UserCaronaModel:

    carona = db.query(Carona).filter(Carona.id == carona_id, Carona.fk_motorista == current_user.id).first()
    if not carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carona não encontrada")
    
    user_carona: UserCarona = db.query(UserCarona).filter(UserCarona.fk_carona == carona.id, UserCarona.fk_user == user_avaliado_id).first()
    if not user_carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado na carona.")
    
    if avaliacao.nota_passageiro > 5 or avaliacao.nota_passageiro < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Valor da avaliação deve ser entre 1 e 5")
    
    user_carona.nota_pasageiro = avaliacao.nota_passageiro
    user_carona.comentário_sobre_passageiro = avaliacao.comentario_passageiro
    
    try:
        db.add(user_carona)
        db.commit()
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro ao criar avaliação sobre passageiro id={user_avaliado_id}")
    
    return user_carona


@router.post("/motorista",response_model=UserCaronaModel, description="Notas de 1 a 5 para avaliação")
def avaliacao_motorista(
    
) -> UserCaronaModel:
    # completar
    return
