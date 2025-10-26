from sqlalchemy import Column, Integer, String, ForeignKey, Table, event, inspect
from sqlalchemy.orm import relationship, backref, object_session

from src.models import Base

MAX_DEPTH = 3


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(Integer, nullable=False, default=1)
    parent_id = Column(
        Integer,
        ForeignKey("activities.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    parent = relationship(
        "Activity",
        remote_side=[id],
        backref=backref("children", cascade="all, delete-orphan"),
    )

    organizations = relationship(
        "Organization",
        secondary="organization_activity",
        back_populates="activities",
    )


organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column(
        "organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE")
    ),
    Column("activity_id", Integer, ForeignKey("activities.id", ondelete="CASCADE")),
)


def _validate_max_depth(target: Activity, is_insert: bool):
    session = object_session(target)
    if session is None:
        return

    if target.parent_id is None:
        target.level = 1
        return

    parent = session.get(Activity, target.parent_id)
    if parent is None:
        raise ValueError(f"Parent activity with id={target.parent_id} not found")

    seen = set()
    current = parent
    while current is not None:
        if current.id in seen:
            raise ValueError("Cycle detected in activity hierarchy")
        seen.add(current.id)
        if current.id == target.id:
            raise ValueError("Cannot set parent to self")
        current = current.parent
        new_level = parent.level + 1
        if new_level > MAX_DEPTH:
            raise ValueError(f"Maximum hierarchy depth of {MAX_DEPTH} exceeded")

        target.level = new_level


@event.listens_for(Activity, "before_insert")
def before_insert_activity(mapper, connection, target: Activity):
    _validate_max_depth(target, is_insert=True)


@event.listens_for(Activity, "before_update")
def before_update_activity(mapper, connection, target: Activity):
    if target.parent_id is not None:
        insp = inspect(target)
        if insp.attrs.parent_id.history.has_changes():
            _validate_max_depth(target, is_insert=False)
        elif target.parent_id is None:
            target.level = 1
