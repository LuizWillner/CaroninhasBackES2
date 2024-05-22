from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint, Boolean, sql
from database import Base


class MotoristaVeiculo(Base):
    __tablename__ = "motorista_veiculo"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fk_motorista = Column(Integer, ForeignKey("motorista.id_fk_user"), index=True, nullable=False)
    fk_veiculo = Column(Integer, ForeignKey("veiculo.id"), index=True, nullable=False)
    placa = Column(String, index=True, nullable=False, unique=False)  # Não é único pois um veículo do motorista desativado poderia repetir
    created_at = Column(DateTime, index=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
    active = Column(Boolean, index=False, nullable=False, server_default=sql.true())
    
    motorista = relationship("Motorista", lazy=True, uselist=False, back_populates="motorista_veiculo")
    veiculo = relationship("Veiculo", lazy=True, uselist=False, back_populates="motorista_veiculo")
    caronas = relationship("Carona", lazy=True, uselist=True, back_populates="veiculo_do_motorista")
    

class Veiculo(Base):
    __tablename__ = "veiculo"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(String, index=True, nullable=False, unique=False)
    marca = Column(String, index=True, nullable=False, unique=False)
    modelo = Column(String, index=True, nullable=False, unique=False)
    cor = Column(String, index=False, nullable=True, unique=False)
    created_at = Column(DateTime, index=False, nullable=False, default=datetime.now)
    
    __table_args__ = (
        UniqueConstraint("tipo", "marca", "modelo", "cor"),
    )
    
    motorista_veiculo = relationship("MotoristaVeiculo", lazy=True, uselist=True, back_populates="veiculo")
    