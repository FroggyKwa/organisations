from typing import Any, Coroutine, Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.buildings import service, exceptions, models


async def get_building_by_id(building_id: int, db: Session = Depends(get_db)) -> type[models.Building]:
    building = db.get(models.Building, building_id)
    if not building:
        raise exceptions.building_not_found()
    return building

