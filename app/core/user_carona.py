from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from fastapi import HTTPException, status
from datetime import datetime

from app.database.user_carona_orm import UserCarona
from app.models.user_carona_oop import UserCaronaCreate, UserCaronaUpdate


def add_user_carona_to_db(user_carona_to_add: UserCaronaCreate, db: Session) -> UserCarona:
    db_user_carona = UserCarona(**user_carona_to_add.dict())
    try:
        db.add(db_user_carona)
        db.commit()
        db.refresh(db_user_carona)
    except SQLAlchemyError as sqlae:
        msg = f"Could not add UserCarona to the database: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    return db_user_carona


def get_user_carona_by_id(db: Session, user_carona_id: int) -> UserCarona:
    return db.query(UserCarona).filter(UserCarona.id == user_carona_id).first()


def get_user_caronas(db: Session, skip: int = 0, limit: int = 10) -> list[UserCarona]:
    return db.query(UserCarona).offset(skip).limit(limit).all()


def update_user_carona_in_db(db: Session, user_carona_id: int, user_carona: UserCaronaUpdate) -> UserCarona:
    db_user_carona = get_user_carona_by_id(db, user_carona_id)
    if not db_user_carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserCarona not found.")
    
    for key, value in user_carona.dict().items():
        setattr(db_user_carona, key, value)
    
    try:
        db.commit()
        db.refresh(db_user_carona)
    except SQLAlchemyError as sqlae:
        msg = f"Could not update UserCarona in the database: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    return db_user_carona


def delete_user_carona_from_db(db: Session, user_carona_id: int) -> UserCarona:
    db_user_carona = get_user_carona_by_id(db, user_carona_id)
    if not db_user_carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserCarona not found.")
    
    try:
        db.delete(db_user_carona)
        db.commit()
    except SQLAlchemyError as sqlae:
        msg = f"Could not delete UserCarona from the database: {sqlae}"
        logging.error(msg)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    return db_user_carona
