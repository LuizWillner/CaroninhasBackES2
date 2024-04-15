from pydantic import BaseModel
from datetime import datetime


class VehicleBase(BaseModel):
    type: str
    brand: str
    model: str
    color: str | None = None
    
class VehicleModel(VehicleBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True


class DriverVehicleBase(BaseModel):
    fk_driver: int
    fk_vehicle: int
    plate: str

class DriverVehicleModel(DriverVehicleBase):
    id: int
    created_at: datetime
    vehicle: VehicleModel
    class Config:
        orm_mode = True