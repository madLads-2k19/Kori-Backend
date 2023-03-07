from sqlalchemy import Column, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from kori.app.db.base import Base


class ProductBilled(Base):
    product_id = Column(ForeignKey("product.id"), primary_key=True)
    version_id = Column(ForeignKey("product_version.version_id"), primary_key=True)
    customer_bill_id = Column(ForeignKey("customer_bill.id"), primary_key=True)
    product_quantity = Column(Numeric)
    total_cost = Column(Numeric)

    product = relationship("Product", back_populates="products_billed")
    product_version = relationship("ProductVersion", back_populates="products_billed")
    customer_bill = relationship("CustomerBill", back_populates="products_billed")
