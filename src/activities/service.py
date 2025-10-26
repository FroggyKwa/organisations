from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import schemas, models, exceptions


def get_activities(db: Session):
    return db.query(models.Activity).all()


def get_activity(db: Session, id: int):
    return db.query(models.Activity).get(id)


def update_activity(
    db: Session, id: int, new_data: schemas.ActivityUpdate
) -> models.Activity:
    activity = get_activity(db, id)
    if activity is None:
        raise exceptions.activity_not_found()
    for field, value in new_data.model_dump(exclude_unset=True).items():
        setattr(activity, field, value)

    db.commit()
    db.refresh(activity)
    return activity


def delete_activity(db: Session, activity: models.Activity) -> models.Activity:
    db.delete(activity)
    db.commit()
    return activity


def create_activity(db: Session, activity: schemas.ActivityCreate) -> models.Activity:
    db_activity = models.Activity(**activity.model_dump())
    db.add(db_activity)
    try:
        db.flush()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    db.commit()
    db.refresh(db_activity)
    return db_activity
