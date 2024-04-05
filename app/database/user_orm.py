from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, UniqueConstraint
from database import Base


class User(Base):
    __tablename__ = "user"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, index=True, nullable=False)
    first_name = Column(String, index=False, nullable=False)
    last_name = Column(String, index=False, nullable=False)
    cpf = Column(String, index=True, nullable=False, unique=True)
    iduff = Column(String, index=True, nullable=True, unique=True)
    hashed_password = Column(String, index=False, nullable=False)
    birthdate = Column(DateTime, index=False, nullable=False)
    created_at = Column(DateTime, index=False, nullable=False, server_default=func.now())
    active = Column(Boolean, index=False, nullable=False, default=True)
    
    driver = relationship('Driver', lazy=False, uselist=False, back_populates="user", cascade="all, delete")
    
    
class Driver(Base):
    __tablename__ = "driver"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fk_user = Column(Integer, ForeignKey("user.id"), index=True, nullable=False, unique=True)
    license = Column(String, index=True, nullable=False, unique=True)
    created_at = Column(DateTime, index=False, nullable=False, server_default=func.now())
    
    user = relationship('User', lazy=False, uselist=False, back_populates="driver")
    driver_vehicle = relationship("DriverVehicle", lazy=True, uselist=True, back_populates="driver", cascade="all, delete")
    