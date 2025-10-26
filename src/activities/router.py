from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import schemas, service, exceptions
from src.database import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.ActivityRead])
def get_activities(db: Session = Depends(get_db)
) -> schemas.ActivityRead:
    return service.get_activities(db)


@router.get("/{id}", response_model=schemas.ActivityRead)
def get_activity(id: int, db: Session = Depends(get_db)) -> schemas.ActivityRead:
    return service.get_activity(db, id)


@router.put("/{id}", response_model=schemas.ActivityRead)
def update_activity(id: int, new_data: schemas.ActivityUpdate, db: Session = Depends(get_db)) -> schemas.ActivityRead:
    return service.update_activity(db, id, new_data)


@router.delete("/{id}", response_model=schemas.ActivityRead)
def delete_activity(id: int, db: Session = Depends(get_db)) -> None:
    activity = service.get_activity(db, id)
    if activity is None:
        raise exceptions.activity_not_found()
    return service.delete_activity(db, activity)


@router.post("/", response_model=schemas.ActivityRead)
def create_activity(
    activity_data: schemas.ActivityCreate, db: Session = Depends(get_db)
) -> schemas.ActivityRead:
    return service.create_activity(db, activity_data)
