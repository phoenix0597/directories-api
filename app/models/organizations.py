from sqlalchemy import Column, Integer, String, ForeignKey, Table, ARRAY
from sqlalchemy.orm import relationship, mapped_column

from app.schemas.activities import activity_to_dict
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
    building_id = mapped_column(
        Integer,
        ForeignKey("buildings.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    phones = Column(ARRAY(String(20)), nullable=True)
    activities = relationship(
        "Activity",
        secondary="organizations_activities",
        back_populates="organizations",
    )

    building = relationship(
        "Building",
        back_populates="organizations",
    )

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "building_id": self.building_id,
    #         "phones": self.phones,
    #         "building": self.building.to_dict() if self.building else None,
    #         "activities": [activity.to_dict() for activity in self.activities],
    #     }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "building_id": self.building_id,
            "building": self.building.to_dict() if self.building else None,
            "activities": [activity_to_dict(activity) for activity in self.activities],
            "phones": self.phones,
        }
