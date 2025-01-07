from sqlalchemy import Column, Integer, String, ForeignKey, Table
from geoalchemy2 import Geography
from sqlalchemy.orm import relationship

from app.db.base import Base


buildings_organizations = Table(
    "buildings_organizations",
    Base.metadata,
    Column("building_id", Integer, ForeignKey("buildings.id")),
    Column(
        "organization_id", Integer, ForeignKey("organizations.id"), primary_key=True
    ),
)


class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    location = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)
    organizations = relationship(
        "Organization", secondary="buildings_organizations", back_populates="building"
    )
