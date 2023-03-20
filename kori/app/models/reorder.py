from uuid import uuid4

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID

from kori.app.db.base import Base


class Reorder(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(ForeignKey("organization.id"))
    store_id = Column(ForeignKey("store.id"))
    product_id = Column(ForeignKey("product.id"))
    reorder_quantity = Column(Numeric)
    reorder_time = Column(TIMESTAMP)
    supplier_paid = Column(Boolean, default=False)
