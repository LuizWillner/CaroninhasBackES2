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

class DriverVehicleModel(BaseModel):
    plate: str
    created_at: datetime
    vehicle: VehicleModel
    class Config:
        orm_mode = True