from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import schemas, models, exceptions


async def get_activities(db: Session):
    return db.query(models.Activity).filter(models.Activity.parent_id.is_(None)).all()


async def create_activity(db: Session, activity: schemas.ActivityCreate) -> models.Activity:
    db_activity = models.Activity(**activity.model_dump())
    db.add(db_activity)
    try:
        db.flush()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    db.commit()
    db.refresh(db_activity)
    return db_activity


async def update_activity(
    db: Session, activity: models.Activity, new_data: schemas.ActivityUpdate
) -> models.Activity:
    if activity is None:
        raise exceptions.activity_not_found()
    for field, value in new_data.model_dump(exclude_unset=True).items():
        setattr(activity, field, value)

    db.commit()
    db.refresh(activity)
    return activity


async def delete_activity(db: Session, activity: models.Activity) -> models.Activity:
    db.delete(activity)
    db.commit()
    return activity
