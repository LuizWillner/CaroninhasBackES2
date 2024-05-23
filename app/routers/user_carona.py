from app.database.carona_orm import Carona
from app.database.user_orm import User
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Annotated
from sqlalchemy.orm import Session

from datetime import datetime
from app.database.user_carona_orm import UserCarona
from app.models.user_carona_oop import UserCaronaBase, UserCaronaUpdate, UserCaronaExtended
from app.utils.db_utils import get_db
from app.core.user_carona import (
    add_user_carona_to_db, 
    get_user_carona_by_id, 
    get_user_caronas, 
    update_user_carona_in_db, 
    delete_user_carona_from_db
)
from app.core.carona import get_carona_by_id
from app.core.authentication import get_current_active_user
from app.models.router_tags import RouterTags


router = APIRouter(prefix="/user-carona", tags=[RouterTags.user_carona])


@router.post("", response_model=UserCaronaExtended)
def add_me_to_carona(
    current_user: Annotated[User, Depends(get_current_active_user)],
    carona: Annotated[Carona, Depends(get_carona_by_id)],
    carona_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> UserCaronaExtended:

    user_carona = add_user_carona_to_db(
        user_carona_to_add=UserCaronaBase(
            fk_user=current_user.id,
            fk_carona=carona_id,
        ),
        db=db
    )
    return user_carona


@router.get("/{user_carona_id}", response_model=UserCaronaExtended)
def read_user_carona(
    user_carona_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> UserCaronaExtended:
    user_carona = get_user_carona_by_id(db=db, user_carona_id=user_carona_id)
    if not user_carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não foi encontrado inscrito na carona.")
    return user_carona


@router.get("/", response_model=List[UserCaronaExtended])
def read_user_caronas(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0, 
    limit: int = 10
) -> List[UserCaronaExtended]:
    return get_user_caronas(db, skip=skip, limit=limit)


@router.put("/{user_carona_id}", response_model=UserCaronaExtended)
def update_user_carona(
    user_carona_id: int,
    user_carona: UserCaronaUpdate,
    db: Annotated[Session, Depends(get_db)]
) -> UserCaronaExtended:
    return update_user_carona_in_db(db=db, user_carona_id=user_carona_id, user_carona=user_carona)


@router.delete("/{user_carona_id}", response_model=UserCaronaExtended)
def delete_user_carona(
    user_carona_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> UserCaronaExtended:
    return delete_user_carona_from_db(db=db, user_carona_id=user_carona_id)


@router.get("", response_model=list[UserCaronaExtended])
def search_caronas_historico(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
) -> list[UserCaronaExtended]:
    caronas = db.query(UserCarona).filter(UserCarona.fk_user == current_user.id).all()
    return caronas
