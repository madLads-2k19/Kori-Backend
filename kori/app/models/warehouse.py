from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from kori.app.db.base import Base


class Warehouse(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(ForeignKey("organization.id"))
    name = Column(String)

    organization = relationship("Organization", back_populates="warehouses")
    warehouse_products = relationship("WarehouseProduct", back_populates="warehouse")
