from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from . import schemas, service, exceptions, models
from src.database import get_db
from .dependencies import get_activity_by_id

router = APIRouter()


@router.get("/", response_model=list[schemas.ActivityRead])
async def get_activities(db: Session = Depends(get_db)) -> schemas.ActivityRead:
    """
    Get all activities
    """
    return service.get_activities(db)


@router.post("/", response_model=schemas.ActivityRead)
async def create_activity(
    activity_data: schemas.ActivityCreate, db: Session = Depends(get_db)
) -> schemas.ActivityRead:
    """
    Create a new activity
    """
    return service.create_activity(db, activity_data)


@router.get("/{activity_id}", response_model=schemas.ActivityRead)
async def get_activity(
    activity: models.Activity = Depends(get_activity_by_id),
) -> schemas.ActivityRead:
    """
    Get a specific activity
    """
    return activity


@router.put("/{activity_id}", response_model=schemas.ActivityRead)
async def update_activity(
    new_data: schemas.ActivityUpdate,
    activity: models.Activity = Depends(get_activity_by_id),
    db: Session = Depends(get_db),
) -> schemas.ActivityRead:
    """
    Update a specific activity
    """
    return await service.update_activity(db, activity, new_data)


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    activity: models.Activity = Depends(get_activity_by_id),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a specific activity
    """
    if activity is None:
        raise exceptions.activity_not_found()
    return service.delete_activity(db, activity)
