from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from kori.app.db.base import Base


class Product(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(ForeignKey("organization.id"))
    reorder_level = Column(Integer)
    is_deleted = Column(Boolean, default=False)

    organization = relationship("Organization", back_populates="products")
    warehouse_products = relationship("WarehouseProduct", back_populates="product")
    store_products = relationship("StoreProduct", back_populates="product")
    product_versions = relationship("ProductVersion", back_populates="product")
    products_billed = relationship("ProductBilled", back_populates="product")
