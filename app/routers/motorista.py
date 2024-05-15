from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session

from app.database.user_orm import User

from app.models.router_tags import RouterTags
from app.models.user_oop import MotoristaBase, UserModel

from app.core.db_utils import get_db
from app.core.motorista import add_motorista_to_db
from app.core.authentication import get_current_active_user


router = APIRouter(tags=[RouterTags.motorista_e_veiculos])


@router.post("/users/me/motorista", response_model=UserModel)
def upgrade_me_to_motorista(
    num_cnh: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
) -> UserModel:
    db_motorista = add_motorista_to_db(
        motorista=MotoristaBase(
            id_fk_user=current_user.id,
            num_cnh=num_cnh
        ),
        db=db
    )
    return current_user