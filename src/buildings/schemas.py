from pydantic import BaseModel


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BuildingBase):
    id: int

    class Config:
        from_attributes = True


class BuildingRead(BuildingBase):
    id: int

    class Config:
        from_attributes = True
