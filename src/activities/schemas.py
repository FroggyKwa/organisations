from typing import Optional

from pydantic import BaseModel, field_validator, ValidationError, ConfigDict


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int
    children: list["ActivityRead"] = []

    model_config = ConfigDict(from_attributes=True)


class ActivityUpdate(BaseModel):
    name: Optional[str]
    parent_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
