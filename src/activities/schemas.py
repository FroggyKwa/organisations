from typing import Optional

from pydantic import BaseModel, field_validator, ValidationError


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int
    children: list["ActivityRead"] = []

    class Config:
        from_attributes = True


class ActivityUpdate(BaseModel):
    name: Optional[str]
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True
