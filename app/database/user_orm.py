from datetime import datetime
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
    fk_user = Column(Integer, ForeignKey("user.id"), unique=True, index=True)
    license = Column(String, index=True, nullable=False, unique=True)
    created_at = Column(DateTime, index=False, nullable=False, server_default=func.now())
    
    user = relationship('User', lazy=False, uselist=False, back_populates="driver")
    driver_vehicle = relationship("DriverVehicle", lazy=True, uselist=True, back_populates="driver", cascade="all, delete")
    

class DriverVehicle(Base):
    __tablename__ = "driver_vehicle"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fk_driver = Column(Integer, ForeignKey("driver.id"), index=True)
    fk_vehicle = Column(Integer, ForeignKey("vehicle.id"), index=True)
    plate = Column(String, index=True, nullable=False, unique=True)
    created_at = Column(DateTime, index=False, nullable=False, server_default=func.now())
    
    driver = relationship("Driver", lazy=True, uselist=False, back_populates="driver_vehicle")
    vehicle = relationship("Vehicle", lazy=True, uselist=False, back_populates="driver_vehicle")
    

class Vehicle(Base):
    __tablename__ = "vehicle"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String, index=True, nullable=False, unique=False)
    brand = Column(String, index=True, nullable=False, unique=False)
    model = Column(String, index=True, nullable=False, unique=False)
    color = Column(String, index=False, nullable=True, unique=False)
    created_at = Column(DateTime, index=False, nullable=False, server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint("type", "brand", "model", "color"),
    )
    
    driver_vehicle = relationship("DriverVehicle", lazy=True, uselist=True, back_populates="vehicle")