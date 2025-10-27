from typing import Any, Coroutine, Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.organizations import service, exceptions, models


async def get_organization_by_id(id: int, db: Session = Depends(get_db)) -> type[models.Organization]:
    organization = db.get(models.Organization, id)
    if not organization:
        raise exceptions.organization_not_found()
    return organization


async def get_phone_by_id(phone_id: int, db: Session = Depends(get_db)):
    phone = db.get(models.Organization, phone_id)
    if not phone:
        raise exceptions.phone_not_found()
    return phone