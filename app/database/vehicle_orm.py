from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from database import Base


class DriverVehicle(Base):
    __tablename__ = "driver_vehicle"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fk_driver = Column(Integer, ForeignKey("driver.id"), index=True, nullable=False)
    fk_vehicle = Column(Integer, ForeignKey("vehicle.id"), index=True, nullable=False)
    plate = Column(String, index=True, nullable=False, unique=True)
    created_at = Column(DateTime, index=False, nullable=False, default=datetime.now)
    
    driver = relationship("Driver", lazy=True, uselist=False, back_populates="driver_vehicle")
    vehicle = relationship("Vehicle", lazy=True, uselist=False, back_populates="driver_vehicle")
    

class Vehicle(Base):
    __tablename__ = "vehicle"
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String, index=True, nullable=False, unique=False)
    brand = Column(String, index=True, nullable=False, unique=False)
    model = Column(String, index=True, nullable=False, unique=False)
    color = Column(String, index=False, nullable=True, unique=False)
    created_at = Column(DateTime, index=False, nullable=False, default=datetime.now)
    
    __table_args__ = (
        UniqueConstraint("type", "brand", "model", "color"),
    )
    
    driver_vehicle = relationship("DriverVehicle", lazy=True, uselist=True, back_populates="vehicle")