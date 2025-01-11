from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    parent_id = Column(
        Integer,
        ForeignKey("activities.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
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
    organizations = relationship(
        "Organization",
        secondary="organizations_activities",
        back_populates="activities",
    )

    def calculate_level(self) -> int:
        """
        Calculate actual level based on parent chain
        :return:
        """
        level = 1
        current = self.parent
        while current is not None:
            level += 1
            current = current.parent
        return level

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "level": self.level,
        }
