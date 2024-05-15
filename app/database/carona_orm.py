from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime, UniqueConstraint
from database import Base


class Carona(Base):
    __tablename__ = "carona"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fk_motorista = Column(Integer, ForeignKey("motorista.id_fk_user"), index=True, nullable=False)
    fk_motorista_veiculo = Column(Integer, ForeignKey("motorista_veiculo.id"), index=True, nullable=False)
    valor = Column(Float, index=True, nullable=False)
    hora_partida = Column(DateTime, index=True, nullable=False)
    created_at = Column(DateTime, index=False, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
    
    motorista = relationship("Motorista", lazy=True, uselist=False, back_populates="caronas")
    veiculo_do_motorista = relationship("MotoristaVeiculo", lazy=True, uselist=False, back_populates="caronas")
    passageiros = relationship("UserCarona", lazy=True, uselist=True, back_populates="carona")
    
    
class UserCarona(Base):
    __tablename__ = "user_carona"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fk_carona = Column(Integer, ForeignKey("carona.id"), index=True, nullable=False)
    fk_user = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    created_at = Column(DateTime, index=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
    
    user = relationship("User", lazy=True, uselist=False, back_populates="inscricao_em_caronas")
    carona = relationship("Carona", lazy=True, uselist=False, back_populates="passageiros")
    
    __table_args__ = (
        UniqueConstraint("fk_carona", "fk_user"),
    )