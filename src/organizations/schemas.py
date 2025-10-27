from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.activities import schemas as activities_schemas
from src.buildings import schemas as buildings_schemas


class PhoneBase(BaseModel):
    number: str


class PhoneCreate(PhoneBase):
    pass


class PhoneRead(PhoneBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PhoneUpdate(PhoneRead):
    pass


class OrganizationBase(BaseModel):
    name: str
    building_id: int


class OrganizationCreate(OrganizationBase):
    phones: list[PhoneCreate]
    activity_ids: list[int]


class OrganizationRead(OrganizationBase):
    id: int
    phones: list[PhoneRead]
    activities: list[activities_schemas.ActivityRead]
    building: buildings_schemas.BuildingRead

    model_config = ConfigDict(from_attributes=True)


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    building_id: Optional[int] = None
    phone_numbers: Optional[list[str]] = None
    activity_ids: Optional[list[int]] = None

    model_config = ConfigDict(from_attributes=True)
