from uuid import uuid4

from sqlalchemy import Column, String, LargeBinary, ForeignKey
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

    organization = relationship("Organization", back_populates="users")
    customer_bills = relationship("CustomerBill", back_populates="user")
