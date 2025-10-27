from typing import Optional

from pydantic import BaseModel, ConfigDict


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class BuildingRead(BuildingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
