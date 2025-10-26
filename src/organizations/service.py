from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import schemas, models, exceptions
from .. import Activity


def get_organizations(db: Session):
    return db.query(models.Organization).all()


def get_organization(db: Session, id: int):
    return db.query(models.Organization).get(id)


def update_organization(
    db: Session, id: int, new_data: schemas.OrganizationUpdate
) -> models.Organization:
    organization = get_organization(db, id)
    if organization is None:
        raise exceptions.organization_not_found()
    for field, value in new_data.model_dump(exclude_unset=True).items():
        setattr(organization, field, value)

    db.commit()
    db.refresh(organization)
    return organization


def delete_organization(
    db: Session, organization: models.Organization
) -> models.Organization:
    db.delete(organization)
    db.commit()
    return organization


def create_organization(
    db: Session, organization: schemas.OrganizationCreate
) -> models.Organization:
    print(organization)
    db_organization = models.Organization(
        **organization.model_dump(exclude={"activity_ids", "phones"})
    )

    if organization.activity_ids:
        db_organization.activities = (
            db.query(Activity).filter(Activity.id.in_(organization.activity_ids)).all()
        )

    if organization.phones:
        db_organization.phones = [
            models.Phone(number=p.number) for p in organization.phones
        ]

    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization
