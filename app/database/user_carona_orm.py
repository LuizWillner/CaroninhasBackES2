from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint, Float, String
from sqlalchemy.orm import relationship
from database import Base


class UserCarona(Base):
    __tablename__ = 'user_carona'
    
    id = Column(Integer, primary_key=True, index=True)
    fk_user = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    fk_carona = Column(Integer, ForeignKey('carona.id'), index=True, nullable=False)
    nota_motorista = Column(Float, index=True,nullable=True)
    nota_passageiro = Column(Float,index= True, nullable=True)
    comentário_sobre_motorista = Column(String,index=True, nullable=True)
    comentário_sobre_passageiro = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())  
    
    __table_args__ = (
        UniqueConstraint("fk_user", "fk_carona"),
    )
    
    user = relationship("User", lazy=True, uselist=False, back_populates="inscricao_em_caronas")
    carona = relationship("Carona", lazy=True, uselist=False, back_populates="passageiros")
