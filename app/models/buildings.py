from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geography
from sqlalchemy.orm import relationship

from app.db.base import Base


class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    location = Column(
        Geography(geometry_type="POINT", srid=4326, spatial_index=True),
        nullable=False,
    )
    organizations = relationship(
        "Organization",
        back_populates="organizations",
        foreign_keys="Organization.building_id",
    )
