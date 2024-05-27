from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime, UniqueConstraint, Boolean, sql
from database import Base


class PedidoCarona(Base):
    __tablename__ = "pedido_carona"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fk_user = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    hora_partida_minima = Column(DateTime, index=True, nullable=False)
    hora_partida_maxima = Column(DateTime, index=True, nullable=False)
    valor = Column(Float, index=True, nullable=False)
    local_partida = Column(String, index=True, nullable=False)
    local_destino = Column(String, index=True, nullable=False)
    fk_carona = Column(Integer, ForeignKey("carona.id"), index=True, nullable=True)
    created_at = Column(DateTime, index=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
    
    user = relationship("User", lazy=True, uselist=False, back_populates="pedidos_de_caronas")
    carona = relationship("Carona", lazy=True, uselist=False, back_populates="pedidos_de_caronas")

    
