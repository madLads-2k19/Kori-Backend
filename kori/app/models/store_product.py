from sqlalchemy import Boolean, Column, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from kori.app.db.base import Base


class StoreProduct(Base):
    product_id = Column(ForeignKey("product.id"), primary_key=True)
    store_id = Column(ForeignKey("store.id"), primary_key=True)
    stock_available = Column(Numeric)
    stock_locked = Column(Numeric)
    reorder_placed = Column(Boolean, default=False)

    store = relationship("Store", back_populates="store_products")
    product = relationship("Product", back_populates="store_products")
