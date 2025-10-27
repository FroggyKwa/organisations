from sqlalchemy.orm import Session

from . import schemas, models, exceptions
from src.organizations.models import Activity


async def get_organizations(db: Session):
    return db.query(models.Organization).all()

async def update_organization(
    db: Session, organization: models.Organization, new_data: schemas.OrganizationUpdate
) -> models.Organization:
    if organization is None:
        raise exceptions.organization_not_found()

    update_data = new_data.model_dump(exclude_unset=True).items()
    if "name" in update_data:
        organization.name = update_data["name"]
    if "building_id" in update_data:
        organization.building_id = update_data["building_id"]

    if "phone_numbers" in update_data:
        organization.phones = [
            models.Phone(number=num) for num in update_data["phone_numbers"]
        ]

    if "activity_ids" in update_data:
        activities = (
            db.query(Activity)
            .filter(Activity.id.in_(update_data["activity_ids"]))
            .all()
        )
        organization.activities = activities

    db.commit()
    db.refresh(organization)
    return organization


async def delete_organization(db: Session, organization: models.Organization) -> None:
    db.delete(organization)
    db.commit()


async def create_organization(
    db: Session, organization: schemas.OrganizationCreate
) -> models.Organization:
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
