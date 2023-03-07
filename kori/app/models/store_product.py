from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from kori.app.db.base import Base


class StoreProduct(Base):
    product_id = Column(ForeignKey("product.id"), primary_key=True)
    store_id = Column(ForeignKey("store.id"), primary_key=True)
    stock_available = Column(Integer)
    stock_locked = Column(Integer)

    store = relationship("Store", back_populates="store_products")
    product = relationship("Product", back_populates="store_products")
