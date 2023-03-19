from uuid import uuid4

from sqlalchemy import Column, ForeignKey, LargeBinary, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from kori.app.db.base import Base


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(ForeignKey("organization.id"))
    name = Column(String)
    email = Column(String)
    pass_hash = Column(LargeBinary)
    permission_level = Column(String)
    default_store_id = Column(ForeignKey("store.id"))

    organization = relationship("Organization", back_populates="users")
    customer_bills = relationship("CustomerBill", back_populates="user")
    default_store = relationship("Store", back_populates="users")
