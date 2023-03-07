from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from kori.app.db.base import Base


class WarehouseProduct(Base):
    product_id = Column(ForeignKey("product.id"), primary_key=True)
    warehouse_id = Column(ForeignKey("warehouse.id"), primary_key=True)
    stock_available = Column(Integer)

    warehouse = relationship("Warehouse", back_populates="warehouse_products")
    product = relationship("Product", back_populates="warehouse_products")
