from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from kori.app.db.base import Base


class ProductVersion(Base):
    product_id = Column(ForeignKey("product.id"), primary_key=True)
    version_id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Numeric)
    measurement_unit = Column(String)
    valid_from = Column(TIMESTAMP)
    valid_to = Column(TIMESTAMP)

    product = relationship("Product", back_populates="product_versions")
    products_billed = relationship("ProductBilled", back_populates="product_version")
