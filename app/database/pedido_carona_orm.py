from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime, UniqueConstraint
from database import Base


class PedidoCarona(Base):
    __tablename__ = "pedido_carona"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fk_user = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    hora_partida_minima = Column(DateTime, index=True, nullable=False)
    hora_partida_maxima = Column(DateTime, index=True, nullable=False)
    coord_partida = Column(String, index=True, nullable=False)
    coord_destino = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, index=False, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
    user = relationship("User", back_populates="pedido_em_caronas")

    
