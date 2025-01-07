from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.base import Base


organizations_activities = Table(
    "organizations_activities",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id")),
    Column("activity_id", Integer, ForeignKey("activities.id"), primary_key=True),
)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    phones = relationship(
        "Phone", back_populates="organization", cascade="all, delete-orphan"
    )
    building = relationship("Building", secondary="buildings_organizations")
    activities = relationship("Activity", secondary="organizations_activities")
