from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base


class User(Base):
    __tablename__ = "user"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, index=True, nullable=False)
    first_name = Column(String, index=False, nullable=False)
    last_name = Column(String, index=False, nullable=False)
    cpf = Column(String, index=True, nullable=False, unique=True)
    iduff = Column(String, index=True, nullable=True, unique=True)
    password = Column(String, index=False, nullable=True)
    birthdate = Column(DateTime, index=False, nullable=False)
    created_at = Column(DateTime, index=False, nullable=False, default=datetime.now)
    active = Column(Boolean, index=False, nullable=False, default=True)
    