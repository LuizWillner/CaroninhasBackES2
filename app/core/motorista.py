from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends, HTTPException, status

from app.core.db_utils import get_db

from app.database.user_orm import User, Motorista
from app.database.veiculo_orm import MotoristaVeiculo

from app.core.authentication import (
    get_current_active_user
)


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

