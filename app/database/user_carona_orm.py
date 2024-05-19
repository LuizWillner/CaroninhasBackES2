from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class UserCarona(Base):
    __tablename__ = 'user_carona'
    id = Column(Integer, primary_key=True, index=True)
    fk_user = Column(Integer, ForeignKey('user.id'), nullable=False)
    fk_carona = Column(Integer, ForeignKey('carona.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    user = relationship("User", back_populates="inscricao_em_caronas")
    carona = relationship("Carona", back_populates="passageiros")
