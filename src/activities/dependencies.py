from typing import Any, Coroutine, Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.activities import service, exceptions, models


async def get_activity_by_id(id: int, db: Session = Depends(get_db)) -> type[models.Activity]:
    activity = db.get(models.Activity, id)
    if not activity:
        raise exceptions.activity_not_found()
    return activity
