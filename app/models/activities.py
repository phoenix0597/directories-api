from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True, index=True)
    level = Column(Integer, nullable=False, default=1)

    children = relationship(
        "Activity", back_populates="parent", cascade="all, delete-orphan"
    )

    parent = relationship(
        "Activity",
        back_populates="children",
        remote_side="[Activity.id]",
        uselist=False,
    )
    relationship(
        "Organization",
        secondary="organizations_activities",
        back_populates="activities",
    )
