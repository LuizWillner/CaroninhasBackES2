from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, UniqueConstraint
from database import Base


class User(Base):
    __tablename__ = "user"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, index=True, nullable=False, unique=True)
    first_name = Column(String, index=False, nullable=False)
    last_name = Column(String, index=False, nullable=False)
    cpf = Column(String, index=True, nullable=False, unique=True)
    iduff = Column(String, index=True, nullable=True, unique=True)
    phone = Column(String, index=True, nullable=False, unique=True)
    hashed_password = Column(String, index=False, nullable=False)
    birthdate = Column(DateTime, index=False, nullable=False)
    created_at = Column(DateTime, index=False, nullable=False, default=datetime.now)
    active = Column(Boolean, index=False, nullable=False, default=True)
    
    motorista = relationship('Motorista', lazy=False, uselist=False, back_populates="user", cascade="all, delete")
    inscricao_em_caronas = relationship("UserCarona", lazy=True, uselist=True, back_populates="user")
    
    
class Motorista(Base):
    __tablename__ = "motorista"
    
    id_fk_user = Column(Integer, ForeignKey("user.id"), primary_key=True, index=True, nullable=False, unique=True)
    num_cnh = Column(String, index=True, nullable=False, unique=True)
    created_at = Column(DateTime, index=False, nullable=False, default=datetime.now)
    
    user = relationship('User', lazy=False, uselist=False, back_populates="motorista")
    motorista_veiculo = relationship("MotoristaVeiculo", lazy=True, uselist=True, back_populates="motorista", cascade="all, delete")
    caronas = relationship("Carona", lazy=True, uselist=True, back_populates="motorista")
    