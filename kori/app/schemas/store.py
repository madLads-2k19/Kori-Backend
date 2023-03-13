from uuid import UUID

from pydantic import BaseModel


class StoreBase(BaseModel):
    name: str
    org_id: UUID


class StoreCreate(StoreBase):
    pass


class StoreUpdate(StoreBase):
    pass


class StoreSchema(StoreBase):
    id: UUID

    class Config:
        orm_mode = True
