from sqlalchemy import Column, Integer, String, ForeignKey, Table, ARRAY
from sqlalchemy.orm import relationship

from app.db.base import Base


organizations_activities = Table(
    "organizations_activities",
    Base.metadata,
    Column(
        "organization_id",
        Integer,
        ForeignKey("organizations.id"),
        primary_key=True,
        index=True,
    ),
    Column(
        "activity_id",
        Integer,
        ForeignKey("activities.id"),
        primary_key=True,
        index=True,
    ),
)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    building_id = Column(
        Integer,
        ForeignKey("buildings.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    phones = Column(ARRAY(String(20)), nullable=True)
    building = relationship(
        "Building", secondary="buildings_organizations", back_populates="organizations"
    )
    activities = relationship(
        "Activity", secondary="organizations_activities", back_populates="organizations"
    )
